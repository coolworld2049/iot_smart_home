import random

from pydantic import BaseModel, Field

from device.schemas import DeviceModel, DeviceState
from device.settings import settings
from device.sensors.base import SimulatorBase


class MotionSensorSimulatorResponse(BaseModel):
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


class MotionSensorSimulator(SimulatorBase):
    def __init__(self, mqtt_broker_host, mqtt_broker_port, mqtt_topic, state):
        super().__init__(mqtt_broker_host, mqtt_broker_port, mqtt_topic, state)

    def measure(self):
        payload = DeviceModel(
            attributes=MotionSensorSimulatorResponse(), state=self.state
        )
        return payload.model_dump_json()


motion = MotionSensorSimulator(
    mqtt_broker_host=settings.mqtt_broker_host,
    mqtt_broker_port=settings.mqtt_broker_port,
    mqtt_topic=settings.mqtt_topic,
    state=DeviceState.on,
)

if __name__ == "__main__":
    motion.run()
