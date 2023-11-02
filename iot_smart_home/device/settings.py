from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    name: str = "SensorDevice"
    description: str = "IOT"
    mqtt_broker_address: str = "localhost"
    mqtt_broker_port: int = 1883
    mqtt_client_name: str = "SensorSimulator"
    measurement_type_include: set[str] | None = None
    measurement_type_exclude: set[str] | None = None
    update_interval: int = 5

    model_config = SettingsConfigDict(
        env_prefix="DEVICE_",
        env_file_encoding="utf-8",
    )


settings = Settings()
