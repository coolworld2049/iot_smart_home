import platform
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field
from uptime import uptime


class DeviceState(str, Enum):
    on: str = "on"
    off: str = "off"


class DeviceBase(BaseModel):
    name: str = platform.node()
    state: DeviceState | None = None
    attributes: Any | None = None
    uptime: float | None = Field(default_factory=lambda: uptime())
    last_changed: str | None = Field(
        default_factory=lambda: datetime.utcnow().__str__()
    )


class MqttDevice(DeviceBase):
    topic: str | None = None


class HttpDevice(DeviceBase):
    url: str
