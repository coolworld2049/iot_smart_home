import asyncio
import pathlib
from contextlib import suppress
from functools import wraps
from typing import Any

from aiogram import types
from aiogram.exceptions import TelegramBadRequest
from fuzzywuzzy import fuzz
from gtts import gTTS
from loguru import logger
from pydub import AudioSegment


def process_handler_error(func):
    async def process_error(e: str, *args, **kwargs):
        logger.exception(e)
        telegram_obj: types.Message | types.CallbackQuery = args[0]
        sleep_time_sec = 2 + round(len(e) / 50, 1)
        text = (
            f"Ошибка:\n\n"
            f"{e.strip()}"
            f"\n\nЭто сообщение будет <b>удалено</b> через <b>{int(sleep_time_sec)} секунды</b>❗"
        )
        telegram_obj_answer = await telegram_obj.answer(text)
        await asyncio.sleep(sleep_time_sec)
        await telegram_obj_answer.delete()
        with suppress(TelegramBadRequest):
            for m_id in range(
                telegram_obj_answer.message_id - 1,
                telegram_obj_answer.message_id + 1,
            ):
                await telegram_obj.bot.delete_message(telegram_obj.from_user.id, m_id)
        try:
            return await func(*args, **kwargs)
        except:
            pass

    @wraps(func)
    async def process_handler_error_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            await process_error(str(e), *args, **kwargs)

    return process_handler_error_wrapper


async def del_prev_message(message):
    with suppress(TelegramBadRequest):
        await message.bot.delete_message(message.from_user.id, message.message_id - 1)


def convert_to_wav(input: pathlib.Path, output_wav: pathlib.Path):
    try:
        ogg_file = AudioSegment.from_file(input, format=input.suffix.replace(".", ""))
        wav_file = ogg_file.set_channels(1).set_frame_rate(44100)
        logger.debug(f"Conversion successful: {input} -> {output_wav}")
        return wav_file.export(output_wav, format="wav")
    except Exception as e:
        logger.error(f"Error during conversion: {e}")


def match_speech_with_cmd(commands: dict[str, Any], voice_text, threshold=90):
    best_match = max(
        list(commands.keys()), key=lambda cmd: fuzz.token_set_ratio(voice_text, cmd)
    )

    if fuzz.token_set_ratio(voice_text, best_match) >= threshold:
        logger.info(f"Matched command: {best_match}")
        return best_match
    else:
        logger.info("No match found.")
        return None


def text_to_wav(text, output_file):
    tts = gTTS(text=text, lang="ru")
    tts.save(output_file)
