from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import admin_search_user_callback


def admin_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text="✉ Рассылка", callback_data="admin:mailing_menu")
    button2 = InlineKeyboardButton(text="📊 Статистика", callback_data="admin:statistic")
    button3 = InlineKeyboardButton(text="⚙ Настройки", callback_data="admin:settings")
    button4 = InlineKeyboardButton(text="🔍 Найти пользователя", callback_data="admin:search_user")
    keyboard.add(button1)
    keyboard.row(button2, button3)
    keyboard.add(button4)
    return keyboard


def admin_mailing_menu_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text="📷 Рассылка с картинкой", callback_data="admin:mailing_with_picture")
    button2 = InlineKeyboardButton(text="🧾 Рассылка без картинки", callback_data="admin:mailing_without_picture")
    button3 = InlineKeyboardButton(text="⏪ Назад", callback_data="admin:back_to_main")
    keyboard.add(button1, button2, button3)
    return keyboard


def admin_settings_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text="💵 Изменить процент комиссии", callback_data="admin:change_markup_percent")
    button2 = InlineKeyboardButton(text="⏪ Назад", callback_data="admin:back_to_main")
    keyboard.add(button1, button2)
    return keyboard


def admin_back_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    button1 = InlineKeyboardButton(text="⏪ Назад", callback_data="admin:back_to_main")
    keyboard.add(button1)
    return keyboard


def admin_search_user_keyboard(user_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text="💳 Изменить баланс",
                                         callback_data=admin_search_user_callback.new(
                                             action="change_balance", user_id=user_id
                                         ))
    button2 = InlineKeyboardButton(text="🔒 Включить подкрутку",
                                         callback_data=admin_search_user_callback.new(
                                             action="on_spinup", user_id=user_id
                                         ))
    button3 = InlineKeyboardButton(text="🔓 Выключить подкрутку",
                                         callback_data=admin_search_user_callback.new(
                                             action="off_spinup", user_id=user_id
                                         ))
    button4 = InlineKeyboardButton(text="💢 Закрыть",
                                   callback_data="close"
                                   )
    keyboard.row(button1)
    keyboard.add(button2, button3)
    keyboard.row(button4)
    return keyboard
