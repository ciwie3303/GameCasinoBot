from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from config import config
from data.functions.Banker import checked_btc
from data.functions.db import update_balance, get_user
from filters.filters import IsPrivate, IsPrivateCall
from keyboards.inline.games_keyboard import understand_keyboard
from keyboards.inline.other_keyboards import deposit_keyboard, output_keyboard
from loader import dp, bot
from states.states import OutputState
import re


@dp.callback_query_handler(IsPrivateCall(), text="deposit")
async def admin_settings(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await call.message.answer(text="Выберите систему пополнения.",
                            reply_markup=deposit_keyboard())


@dp.callback_query_handler(IsPrivateCall(), text="deposit:banker")
async def admin_settings(call: CallbackQuery):
    await call.message.answer("Для оплаты чеком, просто отправьте его в чат.")


@dp.message_handler(IsPrivate())
async def deposit_btc(message: Message):
    if re.search(r'BTC_CHANGE_BOT\?start=', message.text):
        code = re.findall(r'c_\S+', message.text)[0]
        msg =  await checked_btc(message.chat.id, code)
        await message.answer(msg, reply_markup=understand_keyboard())

@dp.callback_query_handler(IsPrivateCall(), text="output")
async def output_1(call: CallbackQuery):
    user_balance = get_user(call.message.chat.id)[1]
    if user_balance >= 100:
        await call.message.answer(f"Введите сумму вывода от 100 до {user_balance} RUB")
        await OutputState.amount.set()
    else:
        await call.message.answer(f"Ваш баланс меньше 100 RUB")


@dp.message_handler(IsPrivate(), state=OutputState.amount)
async def output_2(message: Message, state: FSMContext):
    if message.text.isdigit():
        user_balance = get_user(message.chat.id)[1]
        if 100 <= int(message.text):
            if int(message.text) <= user_balance:
                async with state.proxy() as data:
                    data["amount"] = int(message.text)
                await message.answer(f"Куда вы хотите вывести баланс.",
                                     reply_markup=output_keyboard())
                await OutputState.next()
            else:
                await message.answer(f"❗ На вашем балансе нет данной суммы.")
        else:
            await message.answer(f"❗ Минимальная сумма вывода 100 RUB.")
    else:
        await message.answer(f"❗ Неверный ввод.")

@dp.callback_query_handler(IsPrivateCall(), state=OutputState.place)
async def output_3(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    if call.data == "output:qiwi":
        async with state.proxy() as data:
            data["place"] = "qiwi"
        await call.message.answer(f"Укажите реквезиты для вывода.")
        await OutputState.next()
    elif call.data == "output:banker":
        async with state.proxy() as data:
            amount = data["amount"]
            data["place"] = "banker"
        await call.message.answer(f"💰 Сумма вывода: <b>{amount}</b>\n\n"
                             f"ℹ️Площадка: <b>Banker</b>\n\n"
                                  f"Для подтверждения отправьте <b>+</b>")
        await OutputState.confirm.set()
    elif call.data == "output:cancel":
        await message.answer(f"Вывод успешно отменён.")
        await state.finish()


@dp.message_handler(IsPrivate(), state=OutputState.requesites)
async def output_4(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["requesites"] = message.text
        amount = data["amount"]
    await message.answer(f"💰 Сумма вывода: <b>{amount}</b>\n\n"
                         f"📱 Реквезиты:<b>{message.text}</b>\n\n"
                              f"ℹ️Площадка: <b>QIWI</b>\n\n"
                              f"Для подтверждения отправьте <b>+</b>")
    await OutputState.confirm.set()


@dp.message_handler(IsPrivate(), state=OutputState.confirm)
async def output_4(message: Message, state: FSMContext):
    if message.text == "+":
        async with state.proxy() as data:
            if data["place"] == "qiwi":
                requesites = data["requesites"]
            amount = data["amount"]
            place = data["place"]
        update_balance(message.chat.id, -amount)
        await message.answer("Заявка на вывод успешно сформирована")
        text = f"""Новая заявка на вывод!
Telegram ID: {message.chat.id}
Сумма: {amount}
Площадка: {place}\n"""
        if place == "qiwi":
            text += f"Реквезиты: {requesites}"
        for admin in config("admin_id").split(":"):
            await bot.send_message(chat_id=admin, text=text)
    await state.finish()