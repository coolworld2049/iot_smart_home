import platform
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field
from uptime import uptime

from device.settings import settings


class PhysicalDevice(BaseModel):
    name: str


class DeviceState(str, Enum):
    on: str = "ON"
    off: str = "OFF"


class DeviceModel(BaseModel):
    node: str = platform.node()
    name: str = settings.name
    placement: str | None = settings.placement
    state: DeviceState | str | None = None
    uptime: float | None = Field(default_factory=lambda: uptime())
    last_changed: str = Field(default_factory=lambda: datetime.utcnow().__str__())
    attributes: Any
