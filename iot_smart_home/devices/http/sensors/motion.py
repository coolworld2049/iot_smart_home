import random

from pydantic import BaseModel, Field

from iot_smart_home.devices.http.sensors.base import run


class MotionSensorAttributes(BaseModel):
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


if __name__ == "__main__":
    run(attributes_class=MotionSensorAttributes)
