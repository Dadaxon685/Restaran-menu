from aiogram.types import KeyboardButton,ReplyKeyboardMarkup  ,InlineKeyboardMarkup

keybord = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Kategoriyani qo'shish"), KeyboardButton(text="Mahsulot qo'shish")],
                [KeyboardButton(text="Reklama berish"), KeyboardButton(text="Userlar")]
            ],resize_keyboard= True 
            )