import json
import time
from abc import ABC, abstractmethod

from loguru import logger
from paho.mqtt.client import Client

from device.schemas import DeviceModel, DeviceState
from device.settings import settings


class SimulatorBase(ABC):
    def __init__(
        self,
        mqtt_broker_host,
        mqtt_broker_port,
        mqtt_topic,
        state: DeviceState | None = None,
    ):
        self._client = Client(
            f"{mqtt_broker_host}-{mqtt_broker_port}-{mqtt_topic}", clean_session=True
        )
        self.mqtt_broker_host = mqtt_broker_host
        self.mqtt_broker_port = mqtt_broker_port
        self.mqtt_topic = mqtt_topic
        self.state: DeviceState = state or DeviceState.off

    def on_connect(self, client, userdata, flags, rc):
        self._client = client
        logger.info(f"Connected to {client} with result code {str(rc)}")
        sub_topic = self.mqtt_topic + "/set"
        client.subscribe(sub_topic)
        logger.info(f"Sub to topic {sub_topic}")

    def on_message(self, client, userdata, msg):
        self._client = client
        payload = DeviceModel(**json.loads(msg.payload.decode()))
        if payload.state:
            self.state = payload.state
            logger.info(f"Received state change: {self.state}")
            self.publish(payload.model_dump_json())

    @abstractmethod
    def measure(self) -> str:
        pass

    def publish(self, json_payload: str):
        if not isinstance(json_payload, str):
            raise ValueError(json_payload)
        assert json.dumps(json_payload)
        self._client.publish(self.mqtt_topic, json_payload, qos=0, retain=True)
        logger.info(
            f"Pub to topic '{self.mqtt_topic}' payload {json.dumps(json.loads(json_payload), indent=2)}"
        )

    def __enter__(self):
        self._client.on_connect = self.on_connect
        self._client.on_message = self.on_message
        self._client.connect(self.mqtt_broker_host, self.mqtt_broker_port)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.disconnect()

    def run(self):
        with self:
            try:
                while True and self.state == DeviceState.on:
                    self.publish(self.measure())
                    time.sleep(settings.pub_frequency)
                else:
                    if self.state != DeviceState.on:
                        logger.info(self.state)
            except Exception as e:
                logger.warning(e)
