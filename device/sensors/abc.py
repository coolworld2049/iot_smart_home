import time
import uuid
from abc import ABC, abstractmethod

from loguru import logger
from paho.mqtt.client import Client, MQTTMessage

from device.schemas import DeviceModel, DeviceState
from device.settings import settings


class SensorBase(ABC):
    def __init__(
        self,
        mqtt_broker_host,
        mqtt_broker_port,
        mqtt_topic,
        state: DeviceState | None = None,
    ):
        self.mqtt_broker_host = mqtt_broker_host
        self.mqtt_broker_port = mqtt_broker_port
        self.mqtt_topic = mqtt_topic
        self.state: DeviceState = DeviceState.off or state
        self.topics = [
            self.mqtt_topic + "/state",
        ]

    def on_connect(self, client: Client, userdata, flags, rc):
        logger.info(f"Connected to {client} with result code {str(rc)}")

        for topic in self.topics:
            client.subscribe(topic)
            logger.info(f"Sub to topic {topic}")

    def on_message(self, client: Client, userdata, msg: MQTTMessage):
        logger.info(f"Received from topic '{msg.topic}' message {msg.payload}")
        if msg.payload and msg.topic == f"{self.mqtt_topic}/state":
            device_model = DeviceModel(state=msg.payload.decode())
            logger.info(f"Received state change {device_model.state}")
            self.state = device_model.state
            self.publish(client, device_model.model_dump_json())

    @abstractmethod
    def measure(self) -> str:
        pass

    def publish(self, client: Client, json_payload: str):
        if self.state != DeviceState.on:
            logger.info(self.state)
            return False
        client.publish(self.mqtt_topic, json_payload, qos=0, retain=True)
        logger.info(f"Pub to topic '{self.mqtt_topic}' payload {json_payload}")
        return True

    def __enter__(self):
        client = Client(
            client_id=f"MQTT5-{self.mqtt_broker_host}:{self.mqtt_broker_port}-{uuid.uuid4()}"
        )
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.mqtt_broker_host, self.mqtt_broker_port)
        logger.info("Client connected")
        return client

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info("Client disconnected")

    def run(self):
        with self as client:
            client.loop_start()
            # msg = MQTTMessage(topic="state/set".encode(),)
            # msg.payload = "on".encode()
            # client._on_message(client, None, msg)
            try:
                while True:
                    time.sleep(settings.pub_frequency)
                    self.publish(client, self.measure())
            except KeyboardInterrupt:
                pass
            except Exception as e:
                logger.error(e)
            client.loop_stop()
            client.disconnect()
