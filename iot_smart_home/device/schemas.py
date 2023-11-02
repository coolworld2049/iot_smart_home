import platform
from datetime import datetime

from pydantic import BaseModel


class MeasurementResponse(BaseModel):
    temperature: float | None = None
    pressure: float | None = None
    relative_humidity: float = None


class DeviceResponse(BaseModel):
    node: str = platform.node()
    date: str = datetime.utcnow().__str__()
    measurement: MeasurementResponse
