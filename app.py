import asyncio

from aiogram import executor

from data.functions.functions import game_time
from handlers import dp
from loader import bot


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(game_time(bot))
    executor.start_polling(dp)







