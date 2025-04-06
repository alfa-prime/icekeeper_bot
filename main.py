import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

from app.core import get_settings, setup_bot_commands
from app.commands import uptime_router, status_router

# Настройки
settings = get_settings()

# Инициализация бота и диспетчера
bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)

dp = Dispatcher()
dp.include_router(uptime_router)
dp.include_router(status_router)

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Команда /start — только для админа
@dp.message(CommandStart())
async def cmd_start(message: Message):
    if message.from_user.id != settings.ADMIN_ID:
        await message.answer("⛔️ У тебя нет доступа.")
        return
    await message.answer("✅ IceKeeper запущен и ждёт команд.")


# Точка входа
async def main():
    logger.info("Запуск IceKeeper...")
    await setup_bot_commands(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
