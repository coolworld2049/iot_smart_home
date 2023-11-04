import platform
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field
from uptime import uptime


class DeviceState(str, Enum):
    on: str = "on"
    off: str = "off"


class Device(BaseModel):
    name: str = platform.node()
    topic: str
    uptime: float = Field(default_factory=lambda: uptime())
    last_changed: str = Field(default_factory=lambda: datetime.utcnow().__str__())
    state: DeviceState | None = None
    attributes: Any | None = None