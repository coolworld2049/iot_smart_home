import platform
import socket
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field
from uptime import uptime


class PhysicalDevice(BaseModel):
    name: str


class NodeState(str, Enum):
    on: str = "ON"
    off: str = "OFF"
    undefined: str = "UNDEFINED"


class Node(BaseModel):
    name: str = platform.node()
    topic: str
    frequency: float
    ipv4: str = socket.gethostbyname_ex(platform.node())[2][1]
    uptime: float | None = Field(default_factory=lambda: uptime())


class DeviceResponse(BaseModel):
    node: Node
    physical_device: PhysicalDevice | None = None
    attributes: Any
    state: NodeState = NodeState.on
    last_changed: str = Field(default_factory=lambda: datetime.utcnow().__str__())
