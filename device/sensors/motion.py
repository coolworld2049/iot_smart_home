import random

from pydantic import BaseModel, Field

from device.schemas import DeviceResponse
from device.settings import settings
from device.simulator.base import DeviceSimulator


class Attributes(BaseModel):
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
    detection_distance: str = Field(
        default_factory=lambda: f"{random.choice(list(range(1, 5)))} meters"
    )
    detection_angle: str = Field(
        default_factory=lambda: f"{random.choice(list(range(60, 120)))} degrees"
    )


class SensorResponse(DeviceResponse):
    attributes: Attributes


class MotionSensorSimulator(DeviceSimulator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def measure(self):
        response = SensorResponse(
            node=self._node,
            attributes=Attributes(),
        )
        self.publish(response)
        return response


motion = MotionSensorSimulator(
    topic=settings.mqtt_topic,
    description=settings.description,
    frequency=settings.frequency,
    data_publisher=settings.mqtt_data_publisher,
)

if __name__ == "__main__":
    motion.run()
