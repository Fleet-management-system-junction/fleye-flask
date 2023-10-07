import paho.mqtt.client as mqtt
from controllers.mqtt_controller import MQTTController

client = mqtt.Client()
client.connect("13.38.173.241", 1883, 60)
client.loop_start()
client.on_connect = MQTTController.on_connect
client.on_message = MQTTController.on_message