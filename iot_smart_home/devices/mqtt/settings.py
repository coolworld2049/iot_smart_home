from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    broker_host: str = "localhost"
    broker_port: int = 1883
    broker_username: str | None = None
    broker_password: str | None = None

    pub_frequency: float = 2
    sensor_topic: str = "sensors"
    controller_topic: str = "controller"

    shared_aes_key: str

    model_config = SettingsConfigDict(
        env_prefix="IOT_SMART_HOME_MQTT_",
        env_file_encoding="utf-8",
    )


settings = Settings()
