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
        # Получаем uptime сервера
        uptime = subprocess.check_output("/usr/bin/uptime -p", shell=True, text=True)

        # Получаем информацию о свободном месте на диске
        disk_usage = subprocess.check_output(
            "/usr/bin/df -h | grep -E '^Filesystem|^/dev/vda2' | awk '{print $1, $2, $3, $4, $5}' | column -t",
            shell=True, text=True
        )

        # Получаем информацию о загрузке процессора с помощью mpstat
        cpu_usage = subprocess.check_output(
            "/usr/bin/mpstat -P ALL  1 1 | awk 'NR>6 {print $2, $3, $5, $12, $13}' | column -t",
            shell=True, text=True
        )

        # Получаем среднюю загрузку за последние 1, 5 и 15 минут с помощью uptime
        load_avg = subprocess.check_output("/usr/bin/uptime", shell=True, text=True)

        # Формируем ответ
        status_message = (
            "<b>Server status:</b>\n"
            "<b>Uptime:</b>\n"
            "<code>────────────────────────────────────────────</code>\n"
            f"<code>{uptime}</code>\n"
            "<b>Disk usage:</b>\n"
            "<code>────────────────────────────────────────────</code>\n"
            f"<code>{disk_usage}</code>\n"
            "<b>CPU usage:</b>\n"
            "<code>────────────────────────────────────────────</code>\n"
            f"<code>{cpu_usage}</code>\n\n"
            "<b>Средняя загрузка за последние 1, 5, 15 минут:</b>\n"
            "<code>────────────────────────────────────────────</code>\n"
            f"<pre>{load_avg.strip()}</pre>"
        )

        await message.answer(status_message, parse_mode=ParseMode.HTML)
    except Exception as e:
        # В случае ошибки при выполнении команды
        await message.answer(f"⚠️ Ошибка при получении статуса: {e}")
