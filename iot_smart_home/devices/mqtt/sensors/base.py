import time
from abc import abstractmethod

from loguru import logger
from paho.mqtt.client import Client, MQTTMessage

from iot_smart_home.core._logging import configure_logging
from iot_smart_home.devices.mqtt.base import MqttSecureDeviceBase
from iot_smart_home.core.schemas import DeviceState, Device


class MqttSensorBase(MqttSecureDeviceBase):
    STATE_TOPIC_SUFFIX = "/state"

    def __init__(
        self,
        broker_host,
        broker_port,
        mqtt_topic,
        pub_frequency,
    ):
        super().__init__(broker_host, broker_port)
        self.mqtt_topic = mqtt_topic
        self.state_topic = mqtt_topic + self.STATE_TOPIC_SUFFIX
        self.pub_frequency = pub_frequency
        self.device = Device(state=DeviceState.on, topic=self.mqtt_topic)

    @abstractmethod
    def measure(self, client: Client) -> Device:
        """Measure and return the device state."""
        pass

    def on_connect(self, client: Client, userdata, flags, rc, property):
        client.subscribe(self.state_topic)
        logger.info(f"Subscribed to topic: {self.state_topic}")

    def on_message(self, client: Client, userdata, msg: MQTTMessage):
        msg.payload = self.payload_encryptor.decrypt_payload(msg.payload)
        logger.info(f"Received from topic '{msg.topic}' message {msg.payload}")
        if msg.payload and msg.topic == self.state_topic:
            self.device.state = msg.payload.decode()
            logger.info(f"Received state change {self.device.state}")
            self.publish(client, self.device.model_dump_json())

    def updater(self, client: Client):
        while True:
            obj = self.measure(client)
            if self.device.state == DeviceState.off:
                obj.attributes = None
            self.device = Device(state=self.device.state, topic=self.mqtt_topic)
            self.publish(client, obj.model_dump_json())
            time.sleep(self.pub_frequency)

    def publish(self, client: Client, payload: str):
        logger.info(f"Publish to topic: '{self.mqtt_topic}' payload {payload}")
        payload = self.payload_encryptor.encrypt_payload(payload.encode())
        client.publish(self.mqtt_topic, payload)
