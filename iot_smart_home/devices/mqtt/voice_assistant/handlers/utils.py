import pathlib
from typing import Any

from fuzzywuzzy import fuzz
from gtts import gTTS
from loguru import logger
from pydub import AudioSegment


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
