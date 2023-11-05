import uuid
from abc import ABC, abstractmethod

from loguru import logger
from paho.mqtt.client import Client, MQTTMessage, MQTTv5

from iot_smart_home.crypt import PayloadEncryptor
from iot_smart_home.settings import settings


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
        """Handle the MQTT client's on_connect event."""
        pass

    @abstractmethod
    def on_message(self, client: Client, userdata, msg: MQTTMessage):
        """Handle the MQTT client's on_message event."""
        pass

    @abstractmethod
    def updater(self, client: Client):
        """Update the MQTT client as needed."""
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


class MqttSecureDeviceBase(MqttDeviceBase, ABC):
    def __init__(self, mqtt_broker_host, mqtt_broker_port):
        super().__init__(mqtt_broker_host, mqtt_broker_port)
        self.payload_encryptor = PayloadEncryptor(settings.shared_aes_key)
