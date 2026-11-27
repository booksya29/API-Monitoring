from aiogram import Bot, Dispatcher
from os import getenv
from schemes import User
from dotenv import load_dotenv
from pathlib import Path
from telegram_bot import new_api, user_api
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from telegram_bot import main_keyboard
import asyncio
from database_sys import DataBase
from shedule_task import check_apis_task, sheduler

env_path = Path(__file__).parent.absolute() / ".env"
load_dotenv(env_path)

bot = Bot(token=getenv("BOT_TOKEN"))
dp = Dispatcher()
dp.include_router(user_api.router)
dp.include_router(new_api.router)
dp["db"] = DataBase()


@dp.message(CommandStart())
async def start_message(message:Message, db:DataBase):
    if not db.usersdb_controller.check_user(message.from_user.id):
        data = User(id = message.from_user.id, name = message.from_user.full_name, api_count = 0)
        db.usersdb_controller.add_new_user(data)
    await message.answer("Вітаю! З чого почнемо?", reply_markup=main_keyboard)

async def main():
    sheduler.add_job(check_apis_task, trigger="interval", seconds=10, args = [dp["db"]], max_instances=1, coalesce=True)
    dp["conn"] = dp['db'].connect()
    sheduler.start()
    await dp.start_polling(bot)
    sheduler.shutdown()
    dp["conn"].close()
    dp["db"].close()

if __name__ == "__main__":
    asyncio.run(main())