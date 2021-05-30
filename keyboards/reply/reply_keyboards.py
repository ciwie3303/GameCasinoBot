from aiogram.types import ReplyKeyboardMarkup


def main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("🎮 21 Очко", "🎮 BACCARA")
    keyboard.row("🎲 Игры", "🎰 Slots")
    keyboard.row("🧬 Jackpot")
    keyboard.row("🧑‍💻Кабинет")
    keyboard.row("💫 Отзывы 💫", "🖥 Помощь")
    return keyboard


def play_slots_keyboard(bet):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(f"📍 Крутить | Ставка: {bet}")
    keyboard.row("🔁 Изменить ставку", "⏪ Выход")
    return keyboard

