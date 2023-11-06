from fastapi.routing import APIRouter

from iot_smart_home.devices.http.controller.web.api import mqtt, http

api_router = APIRouter()
api_router.include_router(mqtt.router, prefix="/mqtt", tags=["mqtt"])
api_router.include_router(http.router, prefix="/http", tags=["http"])
