from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_ui_commands(bot: Bot):
    scope = BotCommandScopeAllPrivateChats()
    await bot.delete_my_commands(scope=scope)
    commands = [
        BotCommand(command="hass", description="homeassistant"),
    ]
    await bot.set_my_commands(commands=commands, scope=scope)
