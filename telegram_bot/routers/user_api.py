import math
from aiogram.exceptions import TelegramBadRequest
from pandas import DataFrame
from telegram_bot import build
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from database_sys import DataBase
from telegram_bot import ShowApiList
from telegram_bot import list_apis_keyboard
from io import BytesIO
from aiogram.types import BufferedInputFile

router = Router()

@router.message(F.text == "Перевірити наявні API")
async def show_all_apis(message:Message, state:FSMContext, db:DataBase):
    await state.set_state(ShowApiList.watching)
    data = db.apidb_controller.get_users_api(message.from_user.id)
    message_str = build(data, 0)
    message_out = await message.answer(message_str, reply_markup=list_apis_keyboard)
    await state.update_data(data_from_state=data)
    await state.update_data(message_o=message_out)
    await state.update_data(cur_page=0)

@router.callback_query(F.data == "prev_p", ShowApiList.watching)
async def prev_p_write(callback:CallbackQuery, state:FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    cur_page = state_data.get("cur_page")
    message:Message = state_data.get("message_o")
    data = state_data.get("data_from_state")
    if cur_page > 0:
        cur_page -= 1
        await state.update_data(cur_page=cur_page)
    message_str = build(data,cur_page)
    try:
        await message.edit_text(message_str, reply_markup=list_apis_keyboard)
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
          raise

@router.callback_query(F.data == "next_p", ShowApiList.watching)
async def next_p_write(callback:CallbackQuery, state:FSMContext):
    await callback.answer()
    state_data = await state.get_data()
    cur_page = state_data.get("cur_page")
    message:Message = state_data.get("message_o")
    data = state_data.get("data_from_state")
    if cur_page < (math.ceil(len(data) / 3))-1:
        cur_page += 1
        await state.update_data(cur_page=cur_page)
    message_str = build(data,cur_page)
    try:
        await message.edit_text(message_str, reply_markup=list_apis_keyboard)
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
          raise


@router.message(F.text == "Історія перевірок")
async def show_history(message:Message, db:DataBase):
    df:DataFrame = db.historydb_controller.get_history_by_user(message.from_user.id)
    buffer = BytesIO()
    df.to_csv(buffer, index=False, encoding="utf-8-sig")
    file = BufferedInputFile(buffer.getvalue(), f"{message.from_user.full_name}_history.csv")
    await message.answer_document(file, caption="Ось історія ваших API в csv форматі!")