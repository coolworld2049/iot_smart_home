import platform
import threading
import time
from typing import Type

import requests
import uvicorn
from fastapi import FastAPI
from loguru import logger
from pydantic import BaseModel

from iot_smart_home.core.schemas import HttpDevice, DeviceState
from iot_smart_home.devices.http.settings import settings

device = HttpDevice(url=f"http://{platform.node()}:{settings.port}")

app = FastAPI()
device.state = DeviceState.on


@app.get("/state/{state}")
def device_state(state: str):
    device.state = DeviceState(state)
    return device


def send_http_requests(device: HttpDevice, attributes_class: Type[BaseModel]):
    while True:
        _device = HttpDevice(state=device.state, url=device.url)
        if _device.state == DeviceState.on:
            _device.attributes = attributes_class()
        response = requests.post(
            f"http://{settings.controller_host}:{settings.controller_port}/api/devices",
            json=_device.model_dump(),
        )
        logger.info(
            f"Sent data {_device.model_dump()} Response: {response.status_code}"
        )
        time.sleep(1)


def run(attributes_class: Type[BaseModel]):
    time.sleep(2)
    http_request_thread = threading.Thread(
        target=send_http_requests,
        name=send_http_requests.__name__,
        kwargs={"device": device, "attributes_class": attributes_class},
    )
    http_request_thread.start()
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
    )
