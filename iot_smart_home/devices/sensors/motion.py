import random

from pydantic import BaseModel, Field

from iot_smart_home.devices.sensors.base import MqttSensorBase
from iot_smart_home.settings import settings


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
    def __init__(self, mqtt_broker_host, mqtt_broker_port, mqtt_topic):
        super().__init__(
            mqtt_broker_host,
            mqtt_broker_port,
            mqtt_topic,
            gateway_topic=settings.gateway_topic,
            pub_frequency=settings.pub_frequency,
        )

    def measure(self):
        self.device.attributes = MotionSensorResponse()
        return self.device.model_dump_json()


motion = MotionSensor(
    mqtt_broker_host=settings.mqtt_broker_host,
    mqtt_broker_port=settings.mqtt_broker_port,
    mqtt_topic=settings.mqtt_topic,
)

if __name__ == "__main__":
    motion.run()
