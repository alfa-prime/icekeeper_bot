from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

import subprocess

from app.core import get_settings

# Создаём роутер для регистрации хендлеров (обработчиков команд)
router = Router()

# Загружаем настройки из .env (например, токен и ID админа)
settings = get_settings()


@router.message(Command(commands=["uptime"]))
async def get_uptime(message: Message):
    """
    Обработчик команды /uptime.
    Показывает аптайм сервера в формате "up 1 hour, 24 minutes".

    Проверяет, что команду отправил админ (по Telegram ID),
    иначе — игнорирует запрос.

    Использует subprocess для выполнения системной команды `uptime -p`.
    """
    if message.from_user.id != settings.ADMIN_ID:
        # Неавторизованный пользователь
        await message.answer("⛔️ У тебя нет доступа.")
        return

    try:
        # Выполняем системную команду `uptime -p` (показывает, сколько работает сервер)
        result = subprocess.check_output(["/usr/bin/uptime", "-p"], text=True)

        # Отправляем результат в Telegram
        await message.answer(
            f"Аптайм сервера: `{result.strip()}`",
            parse_mode="Markdown"  # Используем Markdown для оформления
        )

    except Exception as e:
        # В случае ошибки при выполнении команды
        await message.answer(f"⚠️ Ошибка при получении аптайма: {e}")