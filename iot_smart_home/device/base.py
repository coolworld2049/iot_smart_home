from abc import ABCMeta, abstractmethod
from random import gauss, seed, uniform

from iot_smart_home.device.schemas import Measurement, DeviceResponse, Node, NodeState
from iot_smart_home.publisher.mqtt_publisher import DataPublisher


class DeviceSimulator(metaclass=ABCMeta):
    def __init__(
        self,
        name: str,
        description: str = None,
        frequency: int = 1,
        *,
        data_publisher: DataPublisher,
    ):
        self.name = name
        self.description = description
        self.data_publisher = data_publisher
        self._node = Node(state=NodeState.on)
        seed()

    @abstractmethod
    def measure(self):
        pass


class RandomDataGenerator:
    @staticmethod
    def generate_measurement():
        temperature = round(22 + gauss(0, 3), 2)
        pressure = round(101.3 + gauss(0, 5), 2)
        relative_humidity = round(0.35 + uniform(-0.075, 0.075), 2)
        return Measurement(
            temperature=temperature,
            pressure=pressure,
            relative_humidity=relative_humidity,
        )


class DeviceSimulatorImpl(DeviceSimulator):
    def __init__(
        self,
        name: str,
        description: str = None,
        frequency: int = 1,
        *,
        data_publisher: DataPublisher,
        measurement_field_include: set[str] = None,
        measurement_field_exclude: set[str] = None,
    ):
        super().__init__(name, description, frequency, data_publisher=data_publisher)
        self.measurement_field_include = measurement_field_include
        self.measurement_field_exclude = measurement_field_exclude

    def filter_measurement_fields(self, measurement):
        return Measurement(
            **measurement.model_dump(
                include=self.measurement_field_include,
                exclude=self.measurement_field_exclude,
            )
        )

    def measure(self):
        measurement = RandomDataGenerator.generate_measurement()
        filtered_measurement = self.filter_measurement_fields(measurement)
        response = DeviceResponse(node=self._node, measurement=filtered_measurement)
        self.data_publisher.publish(self.name, response.model_dump())
        return response
