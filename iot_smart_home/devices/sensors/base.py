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
        state: DeviceState | None = None,
        *,
        pub_frequency: float,
        gateway_topic: str,
    ):
        super().__init__(mqtt_broker_host, mqtt_broker_port)
        self.mqtt_topic = mqtt_topic
        self.state_topic = self.mqtt_topic + "/state"
        self.pub_frequency = pub_frequency
        self.device = Device(state=state or DeviceState.off, topic=self.mqtt_topic)
        self.gateway_topic = gateway_topic

    @abstractmethod
    def measure(self) -> str:
        pass

    def publish_to_gateway(self, client: Client, subtopic: str = "set"):
        set_topic = f"{self.gateway_topic}/{subtopic}"
        logger.debug(f"Pub to gateway by topic {set_topic}")
        client.publish(set_topic, self.device.model_dump_json(), retain=True)

    def on_connect(self, client: Client, userdata, flags, rc, property):
        logger.info(f"Connected to {client} with result code {str(rc)}")
        client.subscribe(self.state_topic)
        client.subscribe(self.gateway_topic)
        logger.info(f"Sub to topic {self.state_topic}, {self.gateway_topic}")
        self.publish_to_gateway(client)

    def on_message(self, client: Client, userdata, msg: MQTTMessage):
        logger.debug(f"Received from topic '{msg.topic}' message {msg.payload}")
        if msg.payload and msg.topic == f"{self.mqtt_topic}/state":
            self.change_state(client, msg)
            self.publish(client, self.device.model_dump_json())
        if msg.payload and msg.topic == self.gateway_topic:
            self.publish_to_gateway(client)

    def updater(self, client: Client):
        while True:
            time.sleep(self.pub_frequency)
            self.publish(client, self.measure())

    def change_state(self, client: Client, msg: MQTTMessage):
        self.device.state = msg.payload.decode()
        logger.info(f"Received state change {self.device.state}")
        if self.device.state == DeviceState.on:
            self.publish_to_gateway(client)
        elif self.device.state == DeviceState.off:
            self.publish_to_gateway(client, subtopic="delete")

    def publish(self, client: Client, json_payload: str):
        if self.device.state == DeviceState.on:
            client.publish(self.mqtt_topic, json_payload)
            logger.info(f"Pub to topic '{self.mqtt_topic}' payload {json_payload}")
        else:
            logger.info(self.device.state)
