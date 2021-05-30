from aiogram.dispatcher.filters import Command
from telebot.types import Message

from config import config
from data.functions.db import get_user, add_user_to_db
from filters.filters import IsPrivate
from keyboards.inline.admin_menu_keyboards import admin_menu_keyboard
from keyboards.reply.reply_keyboards import main_menu_keyboard
from loader import dp


@dp.message_handler(IsPrivate(), Command("start"))
async def answer_start(message: Message):
    if get_user(message.chat.id) == None:
        add_user_to_db(message.chat.id)
    await message.answer(text="Главное меню",
                         reply_markup=main_menu_keyboard())

@dp.message_handler(IsPrivate(), Command("admin"))
async def admin_menu(message: Message):
    if get_user(message.chat.id) != None:
        if str(message.chat.id) in str(config("admin_id")):
            await message.answer(text="<i>Админ меню</i>",
                                 reply_markup=admin_menu_keyboard())

