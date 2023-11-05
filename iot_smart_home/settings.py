import sys

from dotenv import load_dotenv
from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class MqttSettings(BaseSettings):
    mqtt_broker_host: str = "localhost"
    mqtt_broker_port: int = 1883
    mqtt_topic: str


class Settings(MqttSettings):
    pub_frequency: float = 1
    gateway_topic: str = "gateway"
    controller_topic: str = "controller"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_prefix="IOT_SMART_HOME_",
        env_file_encoding="utf-8",
    )


settings = Settings()
logger.remove()
logger.add(sys.stdout, level=settings.log_level)
