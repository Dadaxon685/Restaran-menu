from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import CRUD
addButton = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Taomlar", callback_data="add"),InlineKeyboardButton(text="Kategoriya qo'shish", callback_data="category"),],
        [InlineKeyboardButton(text="Tekshirish", callback_data="tek")],
    ]
)

tasqidlash = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Tasdiqlash", callback_data="yes"),
            InlineKeyboardButton(text="Bekor qilish", callback_data="no"),
        ]
    ]
)
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from aiogram.utils.keyboard import InlineKeyboardBuilder

def menyular():
    menyu = InlineKeyboardBuilder()
    resteran = CRUD(name='restaran')
    list = resteran.readcategory()
    
    for category_id, category_name in list:
        menyu.button(InlineKeyboardButton(text=category_name, callback_data=str(category_id)))

    menyu.button(InlineKeyboardButton(text="Korzinka", callback_data='korzinka'))
    menyu.button(InlineKeyboardButton(text="Bog'lanish", callback_data='boglanish'))
    menyu.adjust(2)
    return menyu


def Productbutton():
    productbutton = InlineKeyboardBuilder()
    restaran = CRUD(name='restaran')
    category_list = restaran.readcategory()
    for category in category_list:
       productbutton.button(InlineKeyboardButton(text=f"{category[1]} --> {category[0]}", callback_data=f"{category[1]} --> {category[0]}"))

    productbutton.button(text='ortga ',callback_data='ortga')
    productbutton.adjust(3)
    return productbutton

