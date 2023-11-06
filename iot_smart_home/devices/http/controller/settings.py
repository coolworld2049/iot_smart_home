from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8000
    workers_count: int = 1
    reload: bool = False
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_prefix="IOT_SMART_HOME_CONTROLLER_",
        env_file_encoding="utf-8",
    )


controller_settings = Settings()
