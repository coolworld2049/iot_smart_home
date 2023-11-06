import random

from pydantic import BaseModel, Field

from iot_smart_home.devices.http.sensors.base import run


class ClimateSensorAttributes(BaseModel):
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


if __name__ == "__main__":
    run(attributes_class=ClimateSensorAttributes)
