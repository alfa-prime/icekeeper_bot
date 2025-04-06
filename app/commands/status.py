from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
import subprocess

from app.core import get_settings

# Создаём роутер для регистрации хендлеров (обработчиков команд)
router = Router()

# Загружаем настройки из .env (например, токен и ID админа)
settings = get_settings()


@router.message(Command(commands=["status"]))
async def get_uptime(message: Message):
    if message.from_user.id != settings.ADMIN_ID:
        # Неавторизованный пользователь
        await message.answer("⛔️ У тебя нет доступа.")
        return

    try:
        # Получаем информацию о свободном месте на диске
        disk_usage = subprocess.check_output("/usr/bin/df -h", shell=True, text=True)

        # Получаем информацию о загрузке процессора с помощью mpstat
        cpu_usage = subprocess.check_output("/usr/bin/mpstat 1 1", shell=True, text=True)

        # Получаем среднюю загрузку за последние 1, 5 и 15 минут с помощью uptime
        load_avg = subprocess.check_output("/usr/bin/uptime", shell=True, text=True)

        # Формируем ответ
        status_message = (
            f"💾 Статус сервера:\n\n"
            f"Диск:\n{disk_usage}\n\n"
            f"Загрузка процессора:\n{cpu_usage.strip()}\n\n"
            f"Средняя загрузка за последние 1, 5, 15 минут:\n{load_avg.strip()}"
        )

        await message.answer(status_message, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        # В случае ошибки при выполнении команды
        await message.answer(f"⚠️ Ошибка при получении статуса: {e}")
