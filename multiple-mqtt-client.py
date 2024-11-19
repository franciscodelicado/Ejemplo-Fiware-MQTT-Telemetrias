""" Implementa un programa en python que tenga como parámetro obligatorio de entrada "-f" un fichero cvs con la siguiente estructura por fila:
<api_key>;<device_id>;<statistic>;<min_value>;<max_value>

dónde:
    <api_key>: es una cadena formada por una combinación aleatorio de números y letras en minúsculas
    <device_id>: es una cadena de caracteres.
    <statistic>: es un caracter
    <min_value> y <max_value>: son dos valores numéricos que tienen que cumplir que <min_value> < <max_value>

Además el programa podrá tener como parámetros de entrada opcionales
    -h <mqtt_host>: el parámetro <mqtt_host> será la IP o nombre de dominio del servidor MQTT. Por defecto el valor será "localhost"
    -p <mqtt_port>: indica el puerto de escucha del servidor MQTT. Por defecto su valor será 1883

Por cada línea del fichero de entrada, el programa deberá lanzar un "theard" que implemente un cliente mqtt que publique cada segundo valores en el servidor MQTT <mqtt_server> sobre el puerto
<mqtt_port> usando el topic /ul/<api_key>/<device_id>/attrs. El contenido publicado cada segundo seguirá el protocolo UltraLight, y en concreto tendrá la siguiente forma: "<statistic>|<value>".
Dónde <value> es un valor aleatorio calculado entre <min_value> y <max_value> en cada publicación.

El programa deberá hacer una verificación de los parámetros de entrada, validando el formato de los mismos. También deberá validar el contenido del fichero cvs de entrada. En el caso de que o bien los 
parámetros de entrada, o bien el contenido del fichero cvs no sean correctos, el programa deberá mostrar un mensaje de error adecuado al error, e indicar el formato correcto de entrada.
 """

# Importamos las librerías necesarias
import sys
import csv
import threading
import random
import time
import paho.mqtt.client as mqtt

# Definimos una función para validar el formato de los parámetros de entrada
def validar_parametros():
    # Obtenemos los argumentos de la línea de comandos
    args = sys.argv[1:]
    # Creamos un diccionario para almacenar los valores de los parámetros
    params = {}
    # Comprobamos que el primer argumento sea -f y que haya un segundo argumento
    if len(args) >= 2 and args[0] == "-f":
        # Asignamos el valor del segundo argumento al parámetro fichero
        params["fichero"] = args[1]
    else:
        # Si no se cumple la condición, mostramos un mensaje de error y salimos del programa
        print("Error: el parámetro -f es obligatorio y debe ir seguido del nombre del fichero cvs.")
        print("Uso: python programa.py -f fichero.cvs [-h mqtt_host] [-p mqtt_port]")
        sys.exit(1)
    # Recorremos el resto de argumentos buscando los parámetros opcionales -h y -p
    i = 2 # Índice para recorrer la lista de argumentos
    while i < len(args):
        # Comprobamos si el argumento actual es -h y si hay un siguiente argumento
        if args[i] == "-h" and i + 1 < len(args):
            # Asignamos el valor del siguiente argumento al parámetro mqtt_host
            params["mqtt_host"] = args[i + 1]
            # Incrementamos el índice en dos posiciones para saltar el argumento actual y el siguiente
            i += 2
        # Comprobamos si el argumento actual es -p y si hay un siguiente argumento
        elif args[i] == "-p" and i + 1 < len(args):
            # Asignamos el valor del siguiente argumento al parámetro mqtt_port
            params["mqtt_port"] = args[i + 1]
            # Incrementamos el índice en dos posiciones para saltar el argumento actual y el siguiente
            i += 2
        else:
            # Si no se cumple ninguna de las condiciones anteriores, mostramos un mensaje de error y salimos del programa
            print("Error: parámetro no reconocido o faltante.")
            print("Uso: python programa.py -f fichero.cvs [-h mqtt_host] [-p mqtt_port]")
            sys.exit(1)
    # Si no se ha especificado el parámetro mqtt_host, le asignamos el valor por defecto "localhost"
    if "mqtt_host" not in params:
        params["mqtt_host"] = "localhost"
    # Si no se ha especificado el parámetro mqtt_port, le asignamos el valor por defecto 1883
    if "mqtt_port" not in params:
        params["mqtt_port"] = 1883
    # Devolvemos el diccionario con los valores de los parámetros
    return params

# Definimos una función para validar el contenido del fichero cvs de entrada
def validar_fichero(fichero):
    # Creamos una lista vacía para almacenar las líneas válidas del fichero
    lineas = []
    # Intentamos abrir el fichero en modo lectura
    try:
        with open(fichero, "r") as f:
            # Creamos un lector de cvs usando el punto y coma como separador de campos
            reader = csv.reader(f, delimiter=";")
            # Recorremos las filas del fichero
            for fila in reader:
                # Comprobamos que la fila tenga cinco campos
                if len(fila) == 5:
                    # Obtenemos los valores de los campos y los asignamos a variables con nombres descriptivos
                    api_key = fila[0]
                    device_id = fila[1]
                    statistic = fila[2]
                    min_value = fila[3]
                    max_value = fila[4]
                    # Comprobamos que el api_key sea una cadena formada por una combinación aleatoria de números y letras en minúsculas
                    if api_key.isalnum() and api_key.islower():
                        # Comprobamos que el device_id sea una cadena de caracteres (no vacía)
                        if device_id:
                            # Comprobamos que el statistic sea un caracter (no vacío)
                            if statistic and len(statistic) == 1:
                                # Intentamos convertir los valores min_value y max_value a números
                                try:
                                    min_value = float(min_value)
                                    max_value = float(max_value)
                                    # Comprobamos que se cumpla que min_value < max_value
                                    if min_value < max_value:
                                        # Si se cumplen todas las condiciones, añadimos la fila a la lista de líneas válidas
                                        lineas.append(fila)
                                    else:
                                        # Si no se cumple la condición, mostramos un mensaje de error y salimos del programa
                                        print("Error: el valor mínimo debe ser menor que el valor máximo.")
                                        sys.exit(1)
                                except ValueError:
                                    # Si no se puede convertir los valores a números, mostramos un mensaje de error y salimos del programa
                                    print("Error: los valores mínimo y máximo deben ser numéricos.")
                                    sys.exit(1)
                            else:
                                # Si no se cumple la condición, mostramos un mensaje de error y salimos del programa
                                print("Error: el estadístico debe ser un caracter.")
                                sys.exit(1)
                        else:
                            # Si no se cumple la condición, mostramos un mensaje de error y salimos del programa
                            print("Error: el identificador del dispositivo debe ser una cadena de caracteres.")
                            sys.exit(1)
                    else:
                        # Si no se cumple la condición, mostramos un mensaje de error y salimos del programa
                        print("Error: la clave de la API debe ser una combinación aleatoria de números y letras en minúsculas.")
                        sys.exit(1)
                else:
                    # Si no se cumple la condición, mostramos un mensaje de error y salimos del programa
                    print("Error: el fichero cvs debe tener cinco campos por fila separados por punto y coma.")
                    sys.exit(1)
        # Devolvemos la lista de líneas válidas
        return lineas
    except FileNotFoundError:
        # Si no se encuentra el fichero, mostramos un mensaje de error y salimos del programa
        print("Error: el fichero " + fichero + " no existe o no se puede abrir.")
        sys.exit(1)

# Definimos una función para publicar valores aleatorios en el servidor MQTT según los datos de una línea del fichero cvs
def publicar_valores(linea, mqtt_host, mqtt_port):
    # Obtenemos los valores de los campos de la línea y los asignamos a variables con nombres descriptivos
    api_key = linea[0]
    device_id = linea[1]
    statistic = linea[2]
    min_value = float(linea[3])
    max_value = float(linea[4])
    # Creamos un cliente MQTT con el nombre "cliente_" + api_key + "_" + device_id
    client = mqtt.Client("cliente_" + api_key + "_" + device_id)
    # Conectamos el cliente al servidor MQTT con el host y el puerto especificados
    client.connect(mqtt_host, int(mqtt_port))
    # Iniciamos un bucle infinito
    while True:
        # Generamos un valor aleatorio entre min_value y max_value
        value = random.uniform(min_value, max_value)
        # Formateamos el valor con dos decimales
        value = "{:.2f}".format(value)
        # Creamos el mensaje con el formato UltraLight: "<statistic>|<value>"
        message = statistic + "|" + value
        # Publicamos el mensaje en el topic /ul/<api_key>/<device_id>/attrs
        ret=client.publish("/ul/" + api_key + "/" + device_id + "/attrs", message)
        # Comprobamos si se ha publicado correctamente
        if ret.rc == mqtt.MQTT_ERR_SUCCESS:
            # Si se ha publicado correctamente, mostramos un mensaje con el valor publicado
            print("Publicado: " + message)
        else:
            # Si no se ha publicado correctamente, mostramos un mensaje de error y salimos del programa
            print("Error: no se ha podido publicar el mensaje.")
            sys.exit(1)
        # Esperamos un segundo antes de volver a publicar otro valor
        time.sleep(1)

# Obtenemos los valores de los parámetros de entrada llamando a la función validar_parametros()
params = validar_parametros()
# Obtenemos la lista de líneas válidas del fichero cvs llamando a la función validar_fichero()
lineas = validar_fichero(params["fichero"])
# Recorremos las líneas válidas del fichero cvs
for linea in lineas:
    # Creamos un hilo para cada línea que ejecute la función publicar_valores() con los argumentos correspondientes
    hilo = threading.Thread(target=publicar_valores, args=(linea, params["mqtt_host"], params["mqtt_port"]))
    # Iniciamos el hilo
    hilo.start()
