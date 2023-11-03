from device.sensors.climate import climate
from device.sensors.lamp import lamp
from device.sensors.motion import motion


def main():
    climate.run()
    lamp.run()
    motion.run()


if __name__ == "__main__":
    main()
