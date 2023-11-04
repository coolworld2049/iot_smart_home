import time
import uuid
from abc import ABC, abstractmethod

from loguru import logger
from paho.mqtt.client import Client, MQTTMessage, MQTTv5

from iot_smart_home.schemas import Device, DeviceState


class MqttDeviceBase(ABC):
    def __init__(
        self,
        mqtt_broker_host,
        mqtt_broker_port,
    ):
        self.mqtt_broker_host = mqtt_broker_host
        self.mqtt_broker_port = mqtt_broker_port

    def __enter__(self):
        client = Client(
            client_id=f"MQTTv5-{self.mqtt_broker_host}:{self.mqtt_broker_port}-{uuid.uuid4()}",
            protocol=MQTTv5,
        )
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.disconnect()
        client.connect(self.mqtt_broker_host, self.mqtt_broker_port, clean_start=True)
        logger.info("Client connected")
        return client

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info("Client disconnected")

    @abstractmethod
    def on_connect(self, client: Client, userdata, flags, rc, property):
        pass

    @abstractmethod
    def on_message(self, client: Client, userdata, msg: MQTTMessage):
        pass

    @abstractmethod
    def updater(self, client: Client):
        raise NotImplementedError

    def run(self):
        with self as client:
            client.loop_start()
            try:
                self.updater(client)
            except KeyboardInterrupt:
                pass
            except Exception as e:
                logger.error(e)
            finally:
                client.loop_stop()
                client.disconnect()


class MqttSensorBase(MqttDeviceBase, ABC):
    def __init__(
        self,
        mqtt_broker_host,
        mqtt_broker_port,
        mqtt_topic,
        state: DeviceState | None = None,
        *,
        pub_frequency: float,
        discovery_topic: str,
    ):
        super().__init__(mqtt_broker_host, mqtt_broker_port)
        self.mqtt_topic = mqtt_topic
        self.state_topic = self.mqtt_topic + "/state"
        self.discovery_topic = discovery_topic
        self.pub_frequency = pub_frequency
        self.device = Device(state=state or DeviceState.off, topic=self.mqtt_topic)

    @abstractmethod
    def measure(self) -> str:
        pass

    def advertise_to_gateway(self, client: Client):
        set_topic = f"{self.discovery_topic}/set"
        logger.info(f"Advertise to gateway by topic {set_topic}")
        client.publish(set_topic, self.device.model_dump_json(), qos=1)

    def on_connect(self, client: Client, userdata, flags, rc, property):
        logger.info(f"Connected to {client} with result code {str(rc)}")
        client.subscribe(self.state_topic)
        client.subscribe(self.discovery_topic)
        logger.info(f"Sub to topic {self.state_topic}, {self.discovery_topic}")
        self.advertise_to_gateway(client)

    def on_message(self, client: Client, userdata, msg: MQTTMessage):
        logger.info(f"Received from topic '{msg.topic}' message {msg.payload}")
        if msg.payload and msg.topic == f"{self.mqtt_topic}/state":
            self.change_state(client, msg)
        if msg.payload and msg.topic == self.discovery_topic:
            client.publish(self.discovery_topic, self.device.model_dump_json())

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
