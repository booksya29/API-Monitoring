from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from telegram_bot import adding_api_state, exit_keyboard, main_keyboard, method_keyboard, body_keyboard
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
    await message.answer("Введіть тіло запиту у форматі json тексту", reply_markup=body_keyboard)

