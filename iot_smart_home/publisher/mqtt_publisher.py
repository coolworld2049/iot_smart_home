import json

from paho.mqtt import client as mqtt


class DataPublisher:
    def publish(self, topic, data):
        raise NotImplementedError


class MqttDataPublisher(DataPublisher):
    def __init__(self, name: str, broker_address: str, port: int):
        super().__init__()
        self.client = mqtt.Client(name)
        self.client.connect(broker_address, port)

    def publish(self, topic, data):
        if not isinstance(data, str):
            data = json.dumps(data)
        self.client.publish(topic, data)
