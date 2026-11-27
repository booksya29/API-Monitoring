from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



main_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Додати API"), KeyboardButton(text="Перевірити наявні API")]], resize_keyboard=False
)

method_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="GET"), KeyboardButton(text="POST")], [KeyboardButton(text="PATCH"), KeyboardButton(text="PUT")], [KeyboardButton(text="DELETE")]]
)
