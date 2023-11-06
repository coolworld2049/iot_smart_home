import pathlib
import tempfile
import uuid

import speech_recognition as sr
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from loguru import logger

from iot_smart_home.devices.mqtt.voice_assistant.handlers.utils import (
    convert_to_wav,
    match_speech_with_cmd,
    text_to_wav,
)
from iot_smart_home.devices.mqtt.voice_assistant.loader import recognizer, mqtt

router = Router(name=__file__)

commands = {
    "Включи Активируй лампу свет": ("sensors/lamp/state", "on"),
    "Выключи лампу свет": ("sensors/lamp/state", "off"),
    "Включи датчик движения": ("sensors/motion/state", "on"),
    "Выключи датчик движения": ("sensors/motion/state", "off"),
    "Включи датчик климата": ("sensors/climate/state", "on"),
    "Выключи датчик климата": ("sensors/climate/state", "off"),
}


@router.message(F.voice)
@router.message(F.text)
async def hass_voice_control(message: types.Message, state: FSMContext):
    wav_audio_path = None
    if message.voice:
        file = await message.bot.get_file(message.voice.file_id)
        logger.info(file)
        ogg_audio_path = pathlib.Path(tempfile.gettempdir()).joinpath(
            pathlib.Path(file.file_path).with_suffix(".ogg").name
        )
        await message.bot.download_file(file.file_path, destination=ogg_audio_path)
        wav_audio_path = convert_to_wav(
            ogg_audio_path, ogg_audio_path.with_suffix(".wav")
        ).name
    elif message.text:
        mp3_audio_path = pathlib.Path(tempfile.gettempdir()).joinpath(
            pathlib.Path(f"{message.message_id}-text-{uuid.uuid4()}")
            .with_suffix(".mp3")
            .name
        )
        text_to_wav(message.text, mp3_audio_path)
        wav_audio_path = convert_to_wav(
            mp3_audio_path, mp3_audio_path.with_suffix(".wav")
        ).name
    await message.bot.send_chat_action(message.from_user.id, "typing")
    with sr.AudioFile(wav_audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            voice_text = None
            voice_text = recognizer.recognize_google(audio_data, language="ru-RU")
            logger.info(voice_text)
            cmd = match_speech_with_cmd(
                commands=commands,
                voice_text=voice_text,
            )
            if not cmd:
                raise sr.UnknownValueError()
            msg = f"Pub to topic {commands[cmd][0]} payload {commands[cmd][1]}"
            logger.info(msg)
            await message.answer(msg)
            mqtt.publish(commands[cmd][0], commands[cmd][1])
        except sr.UnknownValueError:
            await message.answer("Sorry, I couldn't understand the voice message.")
        except sr.RequestError:
            await message.answer(
                "Sorry, I encountered an error while processing the voice message."
            )
