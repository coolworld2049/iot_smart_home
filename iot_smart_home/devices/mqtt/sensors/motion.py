import random

from paho.mqtt.client import Client
from pydantic import BaseModel, Field

from iot_smart_home.devices.mqtt.sensors.base import MqttSensorBase
from iot_smart_home.devices.mqtt.settings import settings


class MotionSensorResponse(BaseModel):
    motion_detected: bool = Field(default_factory=lambda: random.choice([True, False]))
    light_intensity_lux: float = Field(
        default_factory=lambda: random.uniform(0.0, 1000.0)
    )
    zone_size: str = Field(
        default_factory=lambda: random.choice(["Small", "Medium", "Large"])
    )
    zone_shape: str = Field(
        default_factory=lambda: random.choice(["Square", "Rectangle", "Triangle"])
    )
    detection_distance: int = Field(
        default_factory=lambda: random.choice(list(range(1, 5)))
    )
    detection_angle: int = Field(
        default_factory=lambda: random.choice(list(range(60, 120)))
    )


class MotionSensor(MqttSensorBase):
    def __init__(self, broker_host, broker_port, mqtt_topic):
        super().__init__(
            broker_host,
            broker_port,
            mqtt_topic,
            pub_frequency=settings.pub_frequency,
        )

    def measure(self, client: Client):
        self.device.attributes = MotionSensorResponse()
        return self.device


def main():
    motion = MotionSensor(
        broker_host=settings.broker_host,
        broker_port=settings.broker_port,
        mqtt_topic=settings.sensor_topic,
    )
    motion.run()


if __name__ == "__main__":
    main()
