import random

from pydantic import BaseModel, Field

from device.schemas import DeviceResponse
from device.settings import settings
from device.simulator.base import DeviceSimulator


class Attributes(BaseModel):
    is_on: bool = Field(default_factory=lambda: random.choice([True, False]))
    brightness: int = Field(default_factory=lambda: random.randint(1, 100))
    color_temperature: int = Field(default_factory=lambda: random.randint(2700, 6500))
    color: str = Field(
        default_factory=lambda: random.choice(["Red", "Green", "Blue", "White"])
    )
    mode: str = Field(
        default_factory=lambda: random.choice(["Reading", "Relaxing", "Energizing"])
    )


class SensorResponse(DeviceResponse):
    attributes: Attributes


class LampSensorSimulator(DeviceSimulator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def measure(self):
        response = SensorResponse(
            node=self._node,
            attributes=Attributes(),
        )
        self.publish(response)
        return response


lamp = LampSensorSimulator(
    topic=settings.mqtt_topic,
    description=settings.description,
    frequency=settings.frequency,
    data_publisher=settings.mqtt_data_publisher,
)

if __name__ == "__main__":
    lamp.run()
