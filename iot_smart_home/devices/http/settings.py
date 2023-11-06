import platform
import random

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    device_name: str = platform.node()
    host: str = "127.0.0.1"
    port: int = 8000 + random.randint(10, 99)
    controller_host: str = "127.0.0.1"
    controller_port: int = 8000
    workers_count: int = 1
    reload: bool = False
    log_level: str = "INFO"
    send_frequency: float = 1

    model_config = SettingsConfigDict(
        env_prefix="IOT_SMART_HOME_HTTP_",
        env_file_encoding="utf-8",
    )


settings = Settings()
