from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from telegram_bot import adding_api_state, exit_keyboard, main_keyboard, method_keyboard, body_keyboard, confirm_adding_keyboard
from database_sys import DataBase
import json
from schemes import ApiScheme
router = Router()

@router.callback_query(F.data == "home")
async def home(callback:CallbackQuery):
    await callback.message.answer("Головне меню:", reply_markup=main_keyboard)
    await callback.answer("")

@router.message(F.text == "Додати API")
async def adding_new_api(message:Message, state:FSMContext):
    await message.answer("Починаємо створення API..", reply_markup=ReplyKeyboardRemove())
    await message.answer("Надішліть посилання на API", reply_markup=exit_keyboard)
    await state.set_state(adding_api_state.url)

@router.message(adding_api_state.url)
async def adding_url(message:Message, state:FSMContext):
    if "http" not in message.text:
        await message.answer("Відправте повне посилання включаючи https")
        return
    await state.set_state(adding_api_state.send_method)
    await state.update_data(url = message.text)
    await message.answer("Чудово! Оберіть тип перевірки:", reply_markup=method_keyboard)

@router.message(adding_api_state.send_method)
async def adding_method(message:Message, state:FSMContext):
    if message.text not in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        await message.answer("Оберіть метод з перелічених.")
        return
    await state.update_data(send_method=message.text)
    await state.set_state(adding_api_state.body)
    m = await message.answer("Підготовлюю..", reply_markup=ReplyKeyboardRemove())
    await m.delete()
    await message.answer("Введіть тіло запиту у форматі json тексту", reply_markup=body_keyboard)


@router.callback_query(F.data == "skip", adding_api_state.body)
async def skiping_body(callback:CallbackQuery, state:FSMContext):
    await callback.answer()
    await callback.message.answer("Чудово! Введіть бажану затримку перевірки в секундах(мінімум 360 секунд)")
    await state.update_data(body = "{}")
    await state.set_state(adding_api_state.max_delay_seconds)

@router.message(adding_api_state.body)
async def adding_body(message:Message, state:FSMContext):
    try:
        json.loads(message.text)
    except json.JSONDecodeError:
        await message.answer("Введіть правильний формат JSON.", reply_markup=body_keyboard)
        return

    await message.answer("Чудово! Введіть бажану затримку перевірки в секундах(мінімум 360 секунд)")
    await state.update_data(body = str(message.text))
    await state.set_state(adding_api_state.max_delay_seconds)


@router.message(adding_api_state.max_delay_seconds)
async def finish_adding_api(message:Message, state:FSMContext):
    try:
        data = int(message.text)
        await state.update_data(max_delay = data)
    except ValueError:
        await message.answer("Введіть правильне цілочисельне значення!")
        return
    data = await state.get_data()
    confirm_message = await message.answer(f'Підтвердіть введення:\nПосилання: {data["url"]}\nМетод відправки: {data["send_method"]}\nТіло відправки: {data["body"]}\nЗатримка: {data["max_delay"]}с.', reply_markup=confirm_adding_keyboard)

    await state.set_state(adding_api_state.confirming)


@router.callback_query(F.data == "Yes", adding_api_state.confirming)
async def confirming(callback:CallbackQuery, state:FSMContext, db:DataBase):
    await callback.answer("")
    m = await callback.message.answer("Додаємо вас в базу даних...")
    data = ApiScheme(creator_id=callback.from_user.id, status=True, url = await state.get_value("url"), send_method=await state.get_value("send_method"), body = await state.get_value("body"), max_delay=int(await state.get_value("max_delay")))
    db.apidb_controller.add_new_api(data)
    
    await callback.message.answer('Успішно додано! Що робимо далі?', reply_markup=main_keyboard)
    await m.delete()
    await state.clear()
#{'url': 'http', 'send_method': 'PATCH', 'body': {}, 'max_delay': 360}

@router.callback_query(F.data == "No", adding_api_state.confirming)
async def decline(callback:CallbackQuery, state:FSMContext):
    await state.clear()
    await callback.answer('')
    await callback.message.answer("Відхилено! Що робимо далі?", reply_markup=main_keyboard)