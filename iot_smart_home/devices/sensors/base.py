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

    def advertise_to_gateway(self, client: Client):
        set_topic = f"{self.gateway_topic}/set"
        logger.info(f"Advertise to gateway by topic {set_topic}")
        client.publish(set_topic, self.device.model_dump_json(), qos=1)

    def on_connect(self, client: Client, userdata, flags, rc, property):
        logger.info(f"Connected to {client} with result code {str(rc)}")
        client.subscribe(self.state_topic)
        client.subscribe(self.gateway_topic)
        logger.info(f"Sub to topic {self.state_topic}, {self.gateway_topic}")
        self.advertise_to_gateway(client)

    def on_message(self, client: Client, userdata, msg: MQTTMessage):
        logger.info(f"Received from topic '{msg.topic}' message {msg.payload}")
        if msg.payload and msg.topic == f"{self.mqtt_topic}/state":
            self.change_state(client, msg)
        if msg.payload and msg.topic == self.gateway_topic:
            client.publish(self.gateway_topic, self.device.model_dump_json())

    def updater(self, client: Client):
        while True:
            time.sleep(self.pub_frequency)
            self.publish(client, self.measure())

    def change_state(self, client: Client, msg: MQTTMessage):
        self.device.state = msg.payload.decode()
        logger.info(f"Received state change {self.device.state}")
        self.publish(client, self.device.model_dump_json())
        self.advertise_to_gateway(client)

    def publish(self, client: Client, json_payload: str):
        if self.device.state == DeviceState.on:
            client.publish(self.mqtt_topic, json_payload)
            logger.info(f"Pub to topic '{self.mqtt_topic}' payload {json_payload}")
        else:
            logger.info(self.device.state)
