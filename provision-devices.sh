#!/bin/bash
#
#  curl commands to reload IoT-Agent configuration and sensor descriptions

set -e

printf "⏳ Provisioning IoT devices \n"

#
# Create a service groups for all UltraLight IoT devices
#
curl -s -o /dev/null -X POST 'http://localhost:4041/iot/services' \
-H 'Content-Type: application/json' \
-H 'fiware-service: openiot' \
-H 'fiware-servicepath: /' \
-d '{
    "services":[
        {
            "apikey": "hfa4z89a5phzvp444dsb",
            "cbroker": "http://localhost:1026",
            "entity_type": "Thing",
            "resource":""
        }
    ]
}'


####################################################
#
# Provision sensors 
#

curl -s -o /dev/null -X POST 'http://localhost:4041/iot/devices' \
-H 'Content-Type: application/json' \
-H 'fiware-service: openiot' \
-H 'fiware-servicepath: /' \
-d '{
    "devices": [
        {
            "device_id": "temp001",
            "entity_name": "urn:ngsi-ld:Temperature:001",
            "entity_type": "Temperature",
            "protocol": "PDI-IoTA-UltraLight",
            "transport": "MQTT",
            "timezone": "Europe/Madrid",
            "attributes":[
                {
                    "object_id": "t",
                    "name": "temperature",
                    "type": "Number"}
            ],
            "static_attributes": [
                {
                    "name": "refSensorPoint",
                    "type": "Relationship",
                    "value": "urn:ngsi-ld:SensorPoint:001"
                }
            ]
        },
        {
            "device_id": "temp002",
            "entity_name": "urn:ngsi-ld:Temperature:002",
            "entity_type": "Temperature",
            "protocol": "PDI-IoTA-UltraLight",
            "transport": "MQTT",
            "timezone": "Europe/Madrid",
            "attributes":[
                {
                    "object_id": "t",
                    "name": "temperature",
                    "type": "Number"}
            ],
            "static_attributes": [
                {
                    "name": "refSensorPoint",
                    "type": "Relationship",
                    "value": "urn:ngsi-ld:SensorPoint:002"
                }
            ]
        },
        {
            "device_id": "temp003",
            "entity_name": "urn:ngsi-ld:Temperature:003",
            "entity_type": "Temperature",
            "protocol": "PDI-IoTA-UltraLight",
            "transport": "MQTT",
            "timezone": "Europe/Madrid",
            "attributes":[
                {
                    "object_id": "t",
                    "name": "temperature",
                    "type": "Number"}
            ],
            "static_attributes": [
                {
                    "name": "refSensorPoint",
                    "type": "Relationship",
                    "value": "urn:ngsi-ld:SensorPoint:003"
                }
            ]
        },
        {
            "device_id": "temp004",
            "entity_name": "urn:ngsi-ld:Temperature:004",
            "entity_type": "Temperature",
            "protocol": "PDI-IoTA-UltraLight",
            "transport": "MQTT",
            "timezone": "Europe/Madrid",
            "attributes":[
                {
                    "object_id": "t",
                    "name": "temperature",
                    "type": "Number"}
            ],
            "static_attributes": [
                {
                    "name": "refSensorPoint",
                    "type": "Relationship",
                    "value": "urn:ngsi-ld:SensorPoint:004"
                }
            ]
        },
        {
            "device_id": "luminosity001",
            "entity_name": "urn:ngsi-ld:Luminosity:001",
            "entity_type": "Luminosity",
            "protocol": "PDI-IoTA-UltraLight",
            "transport": "MQTT",
            "timezone": "Europe/Madrid",
            "attributes":[
                {
                    "object_id": "l",
                    "name": "luminosity",
                    "type": "Number"}
            ],
            "static_attributes": [
                {
                    "name": "refSensorPoint",
                    "type": "Relationship",
                    "value": "urn:ngsi-ld:SensorPoint:001"
                }
            ]
        },
        {
            "device_id": "luminosity002",
            "entity_name": "urn:ngsi-ld:Luminosity:002",
            "entity_type": "Luminosity",
            "protocol": "PDI-IoTA-UltraLight",
            "transport": "MQTT",
            "timezone": "Europe/Madrid",
            "attributes":[
                {
                    "object_id": "l",
                    "name": "luminosity",
                    "type": "Number"}
            ],
            "static_attributes": [
                {
                    "name": "refSensorPoint",
                    "type": "Relationship",
                    "value": "urn:ngsi-ld:SensorPoint:002"
                }
            ]
        },
        {
            "device_id": "luminosity003",
            "entity_name": "urn:ngsi-ld:Luminosity:003",
            "entity_type": "Luminosity",
            "protocol": "PDI-IoTA-UltraLight",
            "transport": "MQTT",
            "timezone": "Europe/Madrid",
            "attributes":[
                {
                    "object_id": "l",
                    "name": "luminosity",
                    "type": "Number"}
            ],
            "static_attributes": [
                {
                    "name": "refSensorPoint",
                    "type": "Relationship",
                    "value": "urn:ngsi-ld:SensorPoint:003"
                }
            ]
        }
    ]
}'