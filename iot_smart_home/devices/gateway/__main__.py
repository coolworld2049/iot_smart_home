import json
import time

from loguru import logger
from paho.mqtt.client import Client, MQTTMessage

from iot_smart_home.devices.base import MqttSecureDeviceBase
from iot_smart_home.schemas import Device
from iot_smart_home.settings import settings


class MqttGateway(MqttSecureDeviceBase):
    def __init__(
        self,
        mqtt_broker_host,
        mqtt_broker_port,
        mqtt_topic,
        pooling_timeout: float = 10,
    ):
        super().__init__(mqtt_broker_host, mqtt_broker_port)
        self.mqtt_broker_host = mqtt_broker_host
        self.mqtt_broker_port = mqtt_broker_port
        self.mqtt_topic = mqtt_topic
        self.pooling_timeout = pooling_timeout
        self.devices: dict[str, Device] = {}

    def on_connect(self, client: Client, userdata, flags, rc, property):
        client.subscribe(f"{self.mqtt_topic}/devices")

    def publish_to_devices(self, client: Client):
        topic = "devices"
        devices = {k: v.model_dump() for k, v in self.devices.items()}
        payload = json.dumps(devices)
        payload = self.payload_encryptor.encrypt_payload(payload.encode())
        logger.info(f"Pub to topic '{topic}' payload {payload}")
        client.publish(topic, payload)

    def on_message(self, client: Client, userdata, msg: MQTTMessage):
        logger.info(f"Received from topic '{msg.topic}' message {msg.payload}")
        msg.payload = self.payload_encryptor.decrypt_payload(msg.payload)
        from_device = Device(**json.loads(msg.payload.decode()))
        if msg.topic == f"{self.mqtt_topic}/devices":
            self.devices[from_device.name] = from_device
            self.publish_to_devices(client)

    def updater(self, client: Client):
        while True:
            logger.info(f"Devices {list(self.devices.keys())}")
            time.sleep(self.pooling_timeout)


gateway_controller = MqttGateway(
    settings.mqtt_broker_host,
    settings.mqtt_broker_port,
    mqtt_topic=settings.gateway_topic,
)
if __name__ == "__main__":
    gateway_controller.run()
