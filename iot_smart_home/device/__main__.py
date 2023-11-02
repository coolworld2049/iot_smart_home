import time

from loguru import logger

from iot_smart_home.device.base import MqttDataPublisher, Device
from iot_smart_home.device.settings import settings

mqtt_data_publisher = MqttDataPublisher(
    settings.mqtt_broker_address, settings.mqtt_broker_port
)
iot_device = Device(
    name=settings.name,
    description=settings.description,
    data_publisher=mqtt_data_publisher,
    measurement_type_include=settings.measurement_type_include,
    measurement_type_exclude=settings.measurement_type_exclude,
)


def updater():
    measurement = iot_device.make_measurement()
    logger.info(measurement)


if __name__ == "__main__":
    try:
        while True:
            updater()
            time.sleep(settings.update_interval)
    except Exception as e:
        logger.warning(e)
