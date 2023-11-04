from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class MqttSettings(BaseSettings):
    mqtt_broker_host: str = "localhost"
    mqtt_broker_port: int = 1883
    mqtt_topic: str


class Settings(MqttSettings):
    placement: str | None = None
    pub_frequency: float = 1
    gateway_topic: str = "gateway"

    model_config = SettingsConfigDict(
        env_prefix="IOT_SMART_HOME_",
        env_file_encoding="utf-8",
    )


settings = Settings()
