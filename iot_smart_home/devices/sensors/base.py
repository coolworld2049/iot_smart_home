import time
from abc import ABC, abstractmethod

from loguru import logger
from paho.mqtt.client import Client, MQTTMessage

from iot_smart_home.devices.base import MqttDeviceBase
from iot_smart_home.schemas import DeviceState, Device


class MqttSensorBase(MqttDeviceBase, ABC):
    def __init__(
        self,
        mqtt_broker_host,
        mqtt_broker_port,
        mqtt_topic,
        gateway_topic: str,
        pub_frequency: float,
    ):
        super().__init__(mqtt_broker_host, mqtt_broker_port)
        self.mqtt_topic = mqtt_topic
        self.state_topic = self.mqtt_topic + "/state"
        self.pub_frequency = pub_frequency
        self.device = Device(state=DeviceState.on, topic=self.mqtt_topic)
        self.gateway_topic = gateway_topic

    @abstractmethod
    def measure(self) -> Device:
        pass

    def on_connect(self, client: Client, userdata, flags, rc, property):
        client.subscribe(self.state_topic)
        logger.info(f"Sub to topics: {self.state_topic}")

    def on_message(self, client: Client, userdata, msg: MQTTMessage):
        logger.info(f"Received from topic '{msg.topic}' message {msg.payload}")
        if msg.payload and msg.topic == f"{self.mqtt_topic}/state":
            self.change_state(client, msg)
            self.publish(client, self.device.model_dump_json())

    def updater(self, client: Client):
        while True:
            obj = self.measure()
            if self.device.state == DeviceState.off:
                obj.attributes = None
                logger.warning(f"Device.state={self.device.state}")
            self.publish(client, obj.model_dump_json())
            self.device = Device(state=self.device.state, topic=self.mqtt_topic)
            time.sleep(self.pub_frequency)

    def change_state(self, client: Client, msg: MQTTMessage):
        self.device.state = msg.payload.decode()
        logger.info(f"Received state change {self.device.state}")

    def publish(self, client: Client, json_payload: Device | str):
        topic = f"{self.gateway_topic}/devices"
        client.publish(topic, json_payload)
        logger.info(f"Pub to topic: '{topic}' payload {json_payload}")
