from aiogram import Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware

from iot_smart_home.devices.mqtt.voice_assistant.handlers import homeassistant

dp = Dispatcher(
    name=__file__,
)

dp.callback_query.middleware(CallbackAnswerMiddleware())
dp.include_routers(homeassistant.router)
