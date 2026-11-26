from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

list_apis_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Prev", callback_data='prev_p'), InlineKeyboardButton(text="Next", callback_data="next_p")]]
)