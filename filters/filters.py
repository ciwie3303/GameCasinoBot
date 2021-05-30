from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from config import config


class IsPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE


class IsPrivateCall(BoundFilter):
    async def check(self, call: types.CallbackQuery):
        return call.message.chat.type == types.ChatType.PRIVATE


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        return str(message.from_user.id) in config("admin_id")