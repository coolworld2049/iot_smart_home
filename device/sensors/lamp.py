import random

from pydantic import BaseModel, Field

from device.schemas import DeviceModel, DeviceState
from device.settings import settings
from device.sensors.abc import SensorBase


class LampSensorSimulatorResponse(BaseModel):
    is_on: bool = Field(default_factory=lambda: random.choice([True, False]))
    brightness: int = Field(default_factory=lambda: random.randint(1, 100))
    color_temperature: int = Field(default_factory=lambda: random.randint(2700, 6500))
    color: str = Field(
        default_factory=lambda: random.choice(["Red", "Green", "Blue", "White"])
    )
    mode: str = Field(
        default_factory=lambda: random.choice(["Reading", "Relaxing", "Energizing"])
    )


class LampSensor(SensorBase):
    def __init__(self, mqtt_broker_host, mqtt_broker_port, mqtt_topic, state):
        super().__init__(mqtt_broker_host, mqtt_broker_port, mqtt_topic, state)

    def measure(self):
        payload = DeviceModel(
            attributes=LampSensorSimulatorResponse(), state=self.state
        )
        return payload.model_dump_json()


lamp = LampSensor(
    mqtt_broker_host=settings.mqtt_broker_host,
    mqtt_broker_port=settings.mqtt_broker_port,
    mqtt_topic=settings.mqtt_topic,
    state=DeviceState.on,
)

if __name__ == "__main__":
    lamp.run()
