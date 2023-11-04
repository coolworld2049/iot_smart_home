import uuid

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class MqttSettings(BaseSettings):
    mqtt_broker_host: str = "localhost"
    mqtt_broker_port: int = 1883
    mqtt_client_name: str | None = f"mqtt5-client-{uuid.uuid4()}"
    mqtt_topic: str


class Settings(MqttSettings):
    placement: str | None = None
    pub_frequency: float = 1

    model_config = SettingsConfigDict(
        env_prefix="DEVICE_",
        env_file_encoding="utf-8",
    )


settings = Settings()
