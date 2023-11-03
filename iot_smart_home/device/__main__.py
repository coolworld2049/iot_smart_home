import json
import time

from loguru import logger

from iot_smart_home.device.base import DeviceSimulatorImpl
from iot_smart_home.device.settings import settings
from iot_smart_home.publisher.mqtt_publisher import MqttDataPublisher

mqtt_data_publisher = MqttDataPublisher(
    name=settings.name,
    broker_address=settings.mqtt_broker_address,
    port=settings.mqtt_broker_port,
)
device_simulator = DeviceSimulatorImpl(
    name=settings.name,
    description=settings.description,
    data_publisher=mqtt_data_publisher,
    measurement_field_include=settings.measurement_field_include,
    measurement_field_exclude=settings.measurement_field_exclude,
)


def updater():
    measurement = device_simulator.measure()
    logger.info(json.dumps(measurement.model_dump(), indent=2))


if __name__ == "__main__":
    try:
        while True:
            updater()
            time.sleep(settings.update_interval)
    except Exception as e:
        logger.warning(e)
    except KeyboardInterrupt:
        logger.warning("Exit")
