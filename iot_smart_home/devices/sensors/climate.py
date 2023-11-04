import random

from pydantic import BaseModel, Field

from iot_smart_home.devices.base import MqttSensorBase
from iot_smart_home.schemas import DeviceState
from iot_smart_home.settings import settings


class ClimateSensorResponse(BaseModel):
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


class ClimateSensor(MqttSensorBase):
    def __init__(self, mqtt_broker_host, mqtt_broker_port, mqtt_topic, state):
        super().__init__(
            mqtt_broker_host,
            mqtt_broker_port,
            mqtt_topic,
            state,
            pub_frequency=settings.pub_frequency,
            discovery_topic=settings.discovery_topic,
        )

    def measure(self):
        self.device.attributes = ClimateSensorResponse()
        return self.device.model_dump_json()


climate = ClimateSensor(
    mqtt_broker_host=settings.mqtt_broker_host,
    mqtt_broker_port=settings.mqtt_broker_port,
    mqtt_topic=settings.mqtt_topic,
    state=DeviceState.on,
)

if __name__ == "__main__":
    climate.run()
