import platform
import socket
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field
from uptime import uptime


class MeasurementBase(BaseModel):
    created_at: str = datetime.utcnow().__str__()


class Measurement(MeasurementBase):
    temperature: float | None = None
    pressure: float | None = None
    relative_humidity: float = None


class NodeState(str, Enum):
    on: str = "ON"
    off: str = "OFF"


class Node(BaseModel):
    name: str = platform.node()
    ipv4: str = socket.gethostbyname_ex(platform.node())[2][1]
    uptime: float | None = Field(default_factory=lambda: uptime())
    state: NodeState = NodeState.off


class DeviceResponse(BaseModel):
    node: Node
    measurement: Measurement
