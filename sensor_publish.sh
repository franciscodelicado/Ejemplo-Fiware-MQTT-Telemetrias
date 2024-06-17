#!/bin/bash
export APIKEY_TEMPERATURE=hfa4z89a5phzvp444dsb
export APIKEY_LUMINOSITY=jki23498kadk9234kbkd
export APIKEY_LUMTEMP=abc28304jck13354cds

export BROKER_MQTT=localhost

# Publish temperature
mosquitto_pub -h ${BROKER_MQTT} -t /ul/${APIKEY_TEMPERATURE}/temp001/attrs -m 't|10.5'
mosquitto_pub -h ${BROKER_MQTT} -t /ul/${APIKEY_TEMPERATURE}/temp002/attrs -m 't|20.0'

# Publish luminosity
mosquitto_pub -h ${BROKER_MQTT} -t /ul/${APIKEY_LUMINOSITY}/luminosity001/attrs -m 'l|100'
mosquitto_pub -h ${BROKER_MQTT} -t /ul/${APIKEY_LUMINOSITY}/luminosity002/attrs -m 'l|200'

# Publish temperature and luminosity
mosquitto_pub -h ${BROKER_MQTT} -t /ul/${APIKEY_LUMTEMP}/lumtemp001/attrs -m 't|25.5|l|100'