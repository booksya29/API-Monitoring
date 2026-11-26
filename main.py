from aiogram import Bot, Dispatcher
from os import getenv
from schemes import User
from dotenv import load_dotenv
from pathlib import Path
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
import asyncio
from database_sys import DataBase
env_path = Path(__file__).parent.absolute() / ".env"
load_dotenv(env_path)

bot = Bot(token=getenv("BOT_TOKEN"))
dp = Dispatcher()
dp["db"] = DataBase()

@dp.message(CommandStart())
async def start_message(message:Message, db:DataBase):
    if not db.usersdb_controller.check_user(message.from_user.id):
        data = User(id = message.from_user.id, name = message.from_user.full_name, api_count = 0)
        db.usersdb_controller.add_new_user(data)
    await message.answer("Вітаю! З чого почнемо?")


async def main():
    dp['db'].connect()
    await dp.start_polling(bot)
    dp["db"].close()

if __name__ == "__main__":
    asyncio.run(main())