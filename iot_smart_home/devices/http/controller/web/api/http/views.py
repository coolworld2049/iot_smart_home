from fastapi import APIRouter

from iot_smart_home.devices.http.controller.web.api.mqtt.schema import Message

router = APIRouter()


@router.post("/", response_model=Message)
async def send_echo_message(
    incoming_message: Message,
) -> Message:
    return incoming_message
