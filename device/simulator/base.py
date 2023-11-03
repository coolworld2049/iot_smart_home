import json
import time
from abc import ABCMeta, abstractmethod
from random import seed

from loguru import logger

from device.data_publisher.base import DataPublisher
from device.schemas import Node, DeviceResponse, PhysicalDevice


class DeviceSimulator(metaclass=ABCMeta):
    def __init__(
        self,
        topic: str,
        data_publisher: DataPublisher,
        frequency: float = 1,
        description: str = None,
    ):
        self.topic = topic
        self.description = description
        self.frequency = frequency
        self.data_publisher = data_publisher
        self._node = Node(topic=self.topic, frequency=frequency)
        seed()

    @abstractmethod
    def measure(self):
        pass

    def publish(self, response: DeviceResponse):
        response.physical_device = PhysicalDevice(name=self.__class__.__name__)
        self.data_publisher.publish(self.topic, response.model_dump())

    def run(self):
        try:
            while True:
                measurement = self.measure()
                logger.info(json.dumps(measurement.model_dump(), indent=2))
                time.sleep(self.frequency)
        except Exception as e:
            logger.warning(e)
        except KeyboardInterrupt:
            logger.warning("Exit")
