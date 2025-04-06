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
        disk_usage = subprocess.check_output(
            "/usr/bin/df -h | head -n 1 && /usr/bin/df -h | grep '^/dev/vda2' | awk '{print $1, $2, $3, $4, $5}'",
            shell=True, text=True
        )

        # Получаем информацию о загрузке процессора с помощью mpstat
        cpu_usage = subprocess.check_output("/usr/bin/mpstat 1 1", shell=True, text=True)

        # Получаем среднюю загрузку за последние 1, 5 и 15 минут с помощью uptime
        load_avg = subprocess.check_output("/usr/bin/uptime", shell=True, text=True)

        # Формируем ответ
        status_message = (
            "<b>💾 Статус сервера:</b>\n\n"
            "<b>Диск:</b>\n\n"
            f"<pre>{disk_usage}</pre>\n\n"
            "<b>Загрузка процессора:</b>\n"
            f"<pre>{cpu_usage.strip()}</pre>\n\n"
            "<b>Средняя загрузка за последние 1, 5, 15 минут:</b>\n"
            f"<pre>{load_avg.strip()}</pre>"
        )

        await message.answer(status_message, parse_mode=ParseMode.HTML)
    except Exception as e:
        # В случае ошибки при выполнении команды
        await message.answer(f"⚠️ Ошибка при получении статуса: {e}")
