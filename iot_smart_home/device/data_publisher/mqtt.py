import json

from loguru import logger
from paho.mqtt import client as mqtt

from iot_smart_home.device.data_publisher.base import DataPublisher


class MqttDataPublisher(DataPublisher):
    def __init__(self, client_id: str, host: str, port: int, **connection_kwargs):
        super().__init__()
        self.client = mqtt.Client(client_id)

        self.host = host
        self.port = port

        self.client.connect(self.host, self.port, **connection_kwargs)

    def on_connect(self, userdata, flags, rc):
        logger.info("Connected with result code " + str(rc))

    @staticmethod
    def on_message(userdata, msg):
        logger.info(msg.mqtt_topic + " " + str(msg.payload))

    def startup(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def publish(self, topic, data, **kwargs):
        if not isinstance(data, str):
            data = json.dumps(data)
        self.client.publish(topic, data, **kwargs)
