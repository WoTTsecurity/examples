#!/usr/bin/env python

import os
import paho.mqtt.client as mqtt


MQTT_SERVER = os.getenv('MQTT_SERVER')
MQTT_PORT = int(os.getenv('MQTT_PORT', 8333))
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'wott/temperature')


def on_connect(client, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

client.tls_set(
    ca_certs='/opt/wott/certs/ca.crt',
    certfile='/opt/wott/certs/client.crt',
    keyfile='/opt/wott/certs/client.key'
)


# disables peer verification
# client.tls_insecure_set(True)

# Note that you need to map the ServerDeviceID.d.wott.local to the IP
# of the Docker container running MQTT server
# Do this in /etc/hosts
# The hostname must match the CN (common name) in the certificate.
client.connect(MQTT_SERVER, MQTT_PORT, 60)

client.subscribe(MQTT_TOPIC, 0)

client.loop_forever()
