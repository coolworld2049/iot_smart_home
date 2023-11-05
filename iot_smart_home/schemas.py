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
    topic: str | None = None
    attributes: Any | None = None
    state: DeviceState | None = None
    uptime: float = Field(default_factory=lambda: uptime())
    last_changed: str = Field(default_factory=lambda: datetime.utcnow().__str__())
