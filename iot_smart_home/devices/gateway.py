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

    def discover_devices(self, client: Client):
        pass

    def on_connect(self, client: Client, userdata, flags, rc, property):
        client.subscribe(f"{self.mqtt_topic}/set")
        client.subscribe(f"{self.mqtt_topic}/delete")

    def on_message(self, client: Client, userdata, msg: MQTTMessage):
        logger.info(f"Received from topic '{msg.topic}' message {msg.payload}")
        if not msg.payload:
            raise ValueError(msg)
        device = Device(**json.loads(msg.payload.decode()))
        if msg.topic == f"{self.mqtt_topic}/set":
            self.devices[device.name] = device
            logger.info(f"Added device '{device.name}'")
        if msg.topic == f"{self.mqtt_topic}/delete":
            if self.devices.get(device.name):
                del self.devices[device.name]
                logger.info(f"Removed device '{device.name}'")
        if msg.topic == device.topic:
            logger.info(f"Redirect to topic {device.topic}")
            client.publish(device.topic, msg.payload, msg.qos, msg.retain)

    def updater(self, client: Client):
        while True:
            logger.info(f"Devices {self.devices}")
            self.discover_devices(client)
            time.sleep(self.pooling_timeout)


gateway_controller = MqttGateway(
    settings.mqtt_broker_host,
    settings.mqtt_broker_port,
    mqtt_topic=settings.gateway_topic,
)
if __name__ == "__main__":
    gateway_controller.run()
