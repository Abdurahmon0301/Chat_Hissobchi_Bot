from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


signup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📲 Royxatdan o'tish", callback_data="signup"),
        ]
    ],
)

phone_num = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📞 Telefon raqam yuborish", request_contact=True),
        ]
    ], resize_keyboard=True, one_time_keyboard=True
)