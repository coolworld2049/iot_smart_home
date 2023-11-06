import uuid

import speech_recognition as sr
from aiogram import Bot
from paho.mqtt.client import Client, MQTTv5

from iot_smart_home.devices.mqtt.settings import settings

bot = Bot(token=settings.telegram_bot_token, parse_mode="html")
recognizer = sr.Recognizer()
mqtt = Client(client_id=f"TG-bot-{uuid.uuid4()}", protocol=MQTTv5)
