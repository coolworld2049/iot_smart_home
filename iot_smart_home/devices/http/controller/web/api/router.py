from fastapi.routing import APIRouter

from iot_smart_home.devices.http.controller.web.api import device

api_router = APIRouter()
api_router.include_router(device.router, prefix="/devices", tags=["device"])
