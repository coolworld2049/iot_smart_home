import json
import time

from loguru import logger
from paho.mqtt.client import Client, MQTTMessage
from pydantic import BaseModel

from iot_smart_home.devices.base import MqttDeviceBase
from iot_smart_home.schemas import Device
from iot_smart_home.settings import settings


class MqttGateway(MqttDeviceBase):
    def __init__(
        self,
        mqtt_broker_host,
        mqtt_broker_port,
        discovery_topic,
        pooling_timeout: float = 10,
    ):
        super().__init__(mqtt_broker_host, mqtt_broker_port)
        self.mqtt_broker_host = mqtt_broker_host
        self.mqtt_broker_port = mqtt_broker_port
        self.devices: dict[str, Device] = {}
        self.discovery_topic = discovery_topic
        self.pooling_timeout = pooling_timeout

    def discover_devices(self, client: Client):
        pass

    def on_connect(self, client: Client, userdata, flags, rc, property):
        client.subscribe(f"{self.discovery_topic}/set")

    def on_message(self, client: Client, userdata, msg: MQTTMessage):
        logger.info(f"Received from topic '{msg.topic}' message {msg.payload}")
        if not msg.payload:
            raise ValueError(msg)
        device = Device(**json.loads(msg.payload.decode()))
        if msg.topic == f"{self.discovery_topic}/set":
            self.devices[device.name] = device
        if msg.topic == device.topic:
            client.publish(device.topic, msg.payload, msg.qos, msg.retain)

    def updater(self, client: Client):
        while True:
            devices = json.dumps(
                {k: v.model_dump() for k, v in self.devices.items()}, indent=2
            )
            logger.info(f"Devices {devices}")
            self.discover_devices(client)
            time.sleep(self.pooling_timeout)


if __name__ == "__main__":
    gateway_controller = MqttGateway(
        settings.mqtt_broker_host, settings.mqtt_broker_port, settings.discovery_topic
    )
    gateway_controller.run()
