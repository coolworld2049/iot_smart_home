import requests
from fastapi import APIRouter, Form
from loguru import logger
from starlette.requests import Request
from starlette.responses import RedirectResponse

from iot_smart_home.core.schemas import HttpDevice

router = APIRouter()


@router.get("/")
def get_devices(request: Request) -> dict[str, HttpDevice]:
    return request.app.state.devices


@router.post("/")
def add_device(request: Request, device: HttpDevice) -> HttpDevice:
    logger.info(device)
    state_devices: dict = request.app.state.devices
    state_devices.update({device.name: device})
    return state_devices[device.name]


@router.post("/state")
def switch_device_state(
    request: Request, name: str = Form(), state: str = Form()
) -> RedirectResponse:
    state_devices: dict[str, HttpDevice] = request.app.state.devices
    device = state_devices[name]
    resp = requests.get(f"{device.url}/state/{state}")
    resp.raise_for_status()
    logger.info(f"Device {device.name}: switch state {device.state} to {state}")
    return RedirectResponse("/", status_code=302)
