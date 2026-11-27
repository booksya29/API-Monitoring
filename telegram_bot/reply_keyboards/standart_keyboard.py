from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



main_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Додати API"), KeyboardButton(text="Перевірити наявні API")], [KeyboardButton(text="Історія перевірок")], [KeyboardButton(text="Увімкнути сповіщення"), KeyboardButton(text="Вимкнути сповіщення")]], resize_keyboard=False
)

method_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="GET"), KeyboardButton(text="POST")], [KeyboardButton(text="PATCH"), KeyboardButton(text="PUT")], [KeyboardButton(text="DELETE")]]
)
