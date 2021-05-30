from aiogram.types import Message, InputFile

from config import cabinet_photo
from data.functions.db import get_user
from filters.filters import IsPrivate
from keyboards.inline.other_keyboards import cabinet_keyboard
from loader import dp, bot
from texts import cabinet_text


@dp.message_handler(IsPrivate(), text="🧑‍💻Кабинет")
async def game_menu(message: Message):
    if get_user(message.chat.id) != None:
        await message.answer(cabinet_text(get_user(message.chat.id)),
                             reply_markup=cabinet_keyboard())

@dp.message_handler(IsPrivate(), text="🖥 Помощь")
async def help(message: Message):
    await message.answer("По всем вопросам ➖  @coinBANKER")


@dp.message_handler(IsPrivate(), text="💫 Отзывы 💫")
async def chat(message: Message):
    await message.answer("Отзывы ➖ https://t.me/joinchat/QrmBiMR8779hMTJi")


