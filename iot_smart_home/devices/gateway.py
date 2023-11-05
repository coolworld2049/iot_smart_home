import json
import time

from loguru import logger
from paho.mqtt.client import Client, MQTTMessage

from iot_smart_home.devices.base import MqttDeviceBase
from iot_smart_home.schemas import Device
from iot_smart_home.settings import settings


class MqttGateway(MqttDeviceBase):
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
        client.subscribe(f"devices")

    def publish_to_devices(self, client: Client):
        topic = "devices"
        devices = {k: v.model_dump() for k, v in self.devices.items()}
        client.publish(topic, json.dumps(devices))
        logger.info(f"Pub to topic {topic} payload {json.dumps(devices)}")

    def on_message(self, client: Client, userdata, msg: MQTTMessage):
        logger.info(f"Received from topic '{msg.topic}' message {msg.payload}")
        if not msg.payload:
            raise ValueError(msg)
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
