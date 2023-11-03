import random

from pydantic import BaseModel, Field

from iot_smart_home.device.schemas import DeviceResponse
from iot_smart_home.device.settings import settings
from iot_smart_home.device.simulator.base import DeviceSimulator


class Attributes(BaseModel):
    temperature_celsius: float = Field(
        default_factory=lambda: round(random.uniform(10.0, 35.0), 1)
    )
    humidity_percent: float = Field(
        default_factory=lambda: round(random.uniform(20.0, 80.0), 1)
    )
    air_quality: str = Field(
        default_factory=lambda: random.choice(["Good", "Moderate", "Poor"])
    )
    carbon_dioxide_ppm: int = Field(default_factory=lambda: random.randint(300, 1000))
    air_pressure_hpa: float = Field(
        default_factory=lambda: round(random.uniform(980.0, 1050.0), 1)
    )


class SensorResponse(DeviceResponse):
    attributes: Attributes


class ClimateSensorSimulator(DeviceSimulator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def measure(self):
        response = SensorResponse(
            node=self._node,
            attributes=Attributes(),
        )
        self.publish(response)
        return response


climate = ClimateSensorSimulator(
    topic=settings.mqtt_topic,
    description=settings.description,
    frequency=settings.frequency,
    data_publisher=settings.mqtt_data_publisher,
)
