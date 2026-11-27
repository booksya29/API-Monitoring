from apscheduler.schedulers.asyncio import AsyncIOScheduler
from api_requests import build_check_list
from database_sys import DataBase
import asyncio
sheduler = AsyncIOScheduler()

asyncio.Semaphore(5)

async def check_apis_task(db:DataBase):
    nearest_apis = db.apidb_controller.check_nearest_apis()
    check_func_list = await build_check_list(nearest_apis)
    data = await asyncio.gather(*check_func_list)


