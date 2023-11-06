import random

from pydantic import BaseModel, Field

from iot_smart_home.devices.http.sensors.base import run


class LampSensorAttributes(BaseModel):
    is_on: bool = Field(default_factory=lambda: random.choice([True, False]))
    brightness: int = Field(default_factory=lambda: random.randint(1, 100))
    color_temperature: int = Field(default_factory=lambda: random.randint(2700, 6500))
    color: str = Field(
        default_factory=lambda: random.choice(["Red", "Green", "Blue", "White"])
    )
    mode: str = Field(
        default_factory=lambda: random.choice(["Reading", "Relaxing", "Energizing"])
    )


if __name__ == "__main__":
    run(attributes_class=LampSensorAttributes)
