import random

from paho.mqtt.client import Client
from pydantic import BaseModel, Field

from iot_smart_home.devices.sensors.base import MqttSensorBase
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
    def __init__(self, mqtt_broker_host, mqtt_broker_port, mqtt_topic):
        super().__init__(
            mqtt_broker_host,
            mqtt_broker_port,
            mqtt_topic,
            pub_frequency=settings.pub_frequency,
        )

    def measure(self, client: Client):
        self.device.attributes = ClimateSensorResponse()
        return self.device


def main():
    climate = ClimateSensor(
        mqtt_broker_host=settings.mqtt_broker_host,
        mqtt_broker_port=settings.mqtt_broker_port,
        mqtt_topic=settings.sensor_topic,
    )
    climate.run()


if __name__ == "__main__":
    main()
