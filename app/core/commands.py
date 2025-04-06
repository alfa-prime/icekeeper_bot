from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram import Bot


async def setup_bot_commands(bot: Bot):
    """
    Устанавливает список доступных команд бота (меню Telegram).
    """
    commands = [
        BotCommand(command="start", description="🚀 Запуск IceKeeper"),
        BotCommand(command="uptime", description="🕒 Аптайм сервера"),
        BotCommand(command="disk", description="💾 Состояние диска"),
        BotCommand(command="fail2ban", description="🛡️ Последние заблокированные IP"),
        BotCommand(command="who", description="👤 Кто в системе"),
        BotCommand(command="help", description="📖 Список команд"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())