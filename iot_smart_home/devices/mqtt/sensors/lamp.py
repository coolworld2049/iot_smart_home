import random

from paho.mqtt.client import Client
from pydantic import BaseModel, Field

from iot_smart_home.devices.mqtt.sensors.base import MqttSensorBase
from iot_smart_home.devices.mqtt.settings import settings


class LampSensorResponse(BaseModel):
    is_on: bool = Field(default_factory=lambda: random.choice([True, False]))
    brightness: int = Field(default_factory=lambda: random.randint(1, 100))
    color_temperature: int = Field(default_factory=lambda: random.randint(2700, 6500))
    color: str = Field(
        default_factory=lambda: random.choice(["Red", "Green", "Blue", "White"])
    )
    mode: str = Field(
        default_factory=lambda: random.choice(["Reading", "Relaxing", "Energizing"])
    )


class LampSensor(MqttSensorBase):
    def __init__(self, broker_host, broker_port, mqtt_topic):
        super().__init__(
            broker_host,
            broker_port,
            mqtt_topic,
            pub_frequency=settings.pub_frequency,
        )

    def measure(self, client: Client):
        self.device.attributes = LampSensorResponse()
        return self.device


def main():
    lamp = LampSensor(
        broker_host=settings.broker_host,
        broker_port=settings.broker_port,
        mqtt_topic=settings.sensor_topic,
    )
    lamp.run()


if __name__ == "__main__":
    main()
