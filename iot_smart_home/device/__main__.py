from iot_smart_home.device.sensors.climate import climate
from iot_smart_home.device.sensors.lamp import lamp
from iot_smart_home.device.sensors.motion import motion


def main():
    climate.run()
    lamp.run()
    motion.run()


if __name__ == "__main__":
    main()
