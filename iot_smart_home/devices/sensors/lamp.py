import random

from pydantic import BaseModel, Field

from iot_smart_home.devices.sensors.base import MqttSensorBase
from iot_smart_home.settings import settings


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
    def __init__(self, mqtt_broker_host, mqtt_broker_port, mqtt_topic):
        super().__init__(
            mqtt_broker_host,
            mqtt_broker_port,
            mqtt_topic,
            gateway_topic=settings.gateway_topic,
            pub_frequency=settings.pub_frequency,
        )

    def measure(self):
        self.device.attributes = LampSensorResponse()
        return self.device


def main():
    lamp = LampSensor(
        mqtt_broker_host=settings.mqtt_broker_host,
        mqtt_broker_port=settings.mqtt_broker_port,
        mqtt_topic=settings.sensor_topic,
    )
    lamp.run()


if __name__ == "__main__":
    main()
