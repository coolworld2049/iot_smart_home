import asyncio

from iot_smart_home.core._logging import configure_logging
from iot_smart_home.devices.mqtt.settings import settings
from iot_smart_home.devices.mqtt.voice_assistant.dispatcher import dp
from iot_smart_home.devices.mqtt.voice_assistant.loader import bot, mqtt
from iot_smart_home.devices.mqtt.voice_assistant.ui_commands import set_ui_commands


async def main():
    configure_logging()
    await set_ui_commands(bot)

    mqtt.connect(host=settings.broker_host, port=settings.broker_port)
    mqtt.loop_start()
    await dp.start_polling(bot, polling_timeout=5)
    mqtt.loop_stop()


if __name__ == "__main__":
    asyncio.run(main())
