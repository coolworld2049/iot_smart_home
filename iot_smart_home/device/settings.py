import platform

from pydantic_settings import BaseSettings, SettingsConfigDict

from iot_smart_home.device.data_publisher import mqtt


class MqttSettings(BaseSettings):
    mqtt_broker_address: str = "localhost"
    mqtt_broker_port: int = 1883
    mqtt_client_name: str | None = None
    mqtt_topic: str = "device"

    @property
    def mqtt_data_publisher(self):
        mqtt_data_publisher = mqtt.MqttDataPublisher(
            client_id=settings.name,
            host=settings.mqtt_broker_address,
            port=settings.mqtt_broker_port,
        )
        return mqtt_data_publisher


class Settings(MqttSettings):
    name: str = platform.node()
    description: str | None = None
    frequency: float = 1

    model_config = SettingsConfigDict(
        env_prefix="DEVICE_",
        env_file_encoding="utf-8",
    )


settings = Settings()
