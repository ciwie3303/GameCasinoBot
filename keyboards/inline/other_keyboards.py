from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def cabinet_keyboard():
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text="💳 Пополнить", callback_data="deposit")
    button2 = InlineKeyboardButton(text="💳 Вывести", callback_data="output")
    keyboard.row(button1, button2)

    return keyboard


def deposit_keyboard():
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text="₿ Banker", callback_data="deposit:banker")
    button2 = InlineKeyboardButton(text="Через поддержку", url="t.me/ coinBANKER")
    keyboard.row(button1)
    keyboard.add(button2)

    return keyboard


def output_keyboard():
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text="🥝 Qiwi", callback_data="output:qiwi")
    button2 = InlineKeyboardButton(text="₿ Banker", callback_data="output:banker")
    button3 = InlineKeyboardButton(text="❌ Отмена", callback_data="output:cancel")
    keyboard.row(button1, button2)
    keyboard.row(button3)

    return keyboard

def p2p_deposit_keyboard(bill_id, url):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text='💸 Оплатить 💸', url=url))
    keyboard.add(
        InlineKeyboardButton(text='🔁 Проверить платёж', callback_data=f'check_p2p_deposit:{bill_id}'),
        InlineKeyboardButton(text='❌ Отменить', callback_data=f'reject_p2p_payment')
        )
    return keyboard
