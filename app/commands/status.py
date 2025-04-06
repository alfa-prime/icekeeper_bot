from datetime import datetime

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

        hostname = subprocess.check_output("hostname", shell=True, text=True).strip()
        ip = subprocess.check_output("hostname -I", shell=True, text=True).split()[0]

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

        ram = subprocess.check_output(
            "free -h | awk 'NR==2 {print $2, $3, $4, $7}'",
            shell=True, text=True
        ).strip()
        total, used, free, available = ram.split()
        memory_usage = f"Total: {total}\nUsed: {used}\nFree: {free}\nAvailable: {available}"

        docker_images = subprocess.check_output(
            "docker ps --format '{{.Names}} ({{.Status}})'",
            shell=True, text=True
        )

        last_reboot = subprocess.check_output(
            "/usr/bin/who -b | awk '{print $3, $4}'",
            shell=True, text=True
        )

        # Формируем ответ
        status_message = (
            f"<code><b>🖥️ Host:{hostname} ip: {ip} status</b></code>\n"
            "<code>────────────────────────────────────</code>\n"
            "<b>⏱️ Uptime:</b>\n\n"
            f"<code>{uptime}</code>"
            "<code>────────────────────────────────────</code>\n"
            "<b>🧠 CPU:</b>\n\n"
            f"<code>{cpu_usage}</code>"
            "<code>────────────────────────────────────</code>\n"
            "<b>🧮 Memory:</b>\n\n"
            f"<code>{memory_usage}</code>\n"
            "<code>────────────────────────────────────</code>\n"
            "<b>💾 Disk:</b>\n\n"
            f"<code>{disk_usage}</code>"
            "<code>────────────────────────────────────</code>\n"
            "<b>🐳 Docker:</b>\n\n"
            f"<code>{docker_images}</code>"
            "<code>────────────────────────────────────</code>\n"
            f"<code><b>🔥 Last reboot:</b> {last_reboot}</code>\n"
        )
        await message.answer(status_message, parse_mode=ParseMode.HTML)
    except Exception as e:
        # В случае ошибки при выполнении команды
        await message.answer(f"⚠️ Ошибка при получении статуса: {e}")
