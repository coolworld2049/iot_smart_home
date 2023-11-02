import json
import os
from abc import ABCMeta, abstractmethod
from random import gauss, seed, uniform

import paho.mqtt.client as mqtt

from iot_smart_home.device.schemas import MeasurementResponse, DeviceResponse


class DataPublisher:
    def publish(self, topic, data):
        pass


class MqttDataPublisher(DataPublisher):
    def __init__(self, broker_address, port):
        self.client = mqtt.Client("SensorSimulator")
        self.client.connect(broker_address, port)

    def publish(self, topic, data):
        payload = json.dumps(data)
        self.client.publish(topic, payload)


class DeviceBase(metaclass=ABCMeta):
    def __init__(self, name, frequency=1, description=None):
        self.name = name
        self.host = os.name
        self.description = description

    @abstractmethod
    def make_measurement(self):
        raise NotImplementedError


class Device(DeviceBase):
    def __init__(
        self,
        name,
        description,
        data_publisher: DataPublisher,
        measurement_type_include: set[str] = None,
        measurement_type_exclude: set[str] = None,
    ):
        super().__init__(name, description)
        self.name = name
        self.description = description
        self.data_publisher = data_publisher
        self.measurement_type_include = measurement_type_include
        self.measurement_type_exclude = measurement_type_exclude
        seed()

    def make_measurement(self):
        _ms = MeasurementResponse(
            temperature=round(22 + gauss(0, 3), 2),
            pressure=round(101.3 + gauss(0, 5), 2),
            relative_humidity=round(0.35 + uniform(-0.075, 0.075), 2),
        )
        ms = MeasurementResponse(**_ms.model_dump(
            include=self.measurement_type_include,
            exclude=self.measurement_type_exclude,
        ))
        resp = DeviceResponse(measurement=ms)
        self.data_publisher.publish(self.name, resp.model_dump())
        return resp
