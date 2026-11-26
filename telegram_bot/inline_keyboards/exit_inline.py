from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



exit_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Головне меню", callback_data="home")]])

body_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Пропустити", callback_data="skip")]])

confirm_adding_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Підтвердити", callback_data="Yes")], [InlineKeyboardButton(text="Відхиляю", callback_data="No")]]
)