from aiogram import Bot, F, Dispatcher
from aiogram.types import Message, CallbackQuery, KeyboardButton
import asyncio
import logging
from aiogram.filters.command import CommandStart
from config import bot_token, Admin, User
from butom import admin, orqa, menyu, tekshir
from sqlite3 import connect, Error
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder


logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_token)
dp = Dispatcher()


def createCategory():
    try:
        ulash = connect("restaran")
        cursor = ulash.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS category(
                    name text primary key not null
                    );
                       """)
        ulash.commit()
    except (Exception, Error) as error:
        print(f"Xato: \n\n{error}")
    finally:
        if ulash:
            cursor.close()
            ulash.close()
createCategory()
def createproduct():
    try:
        ulash = connect("restaran")
        cursor = ulash.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS maxsulot(
                    name text primary key not null,
                    narxi int not null,
                    rasmi text not null,
                    category_name text not null
                    );
                       """)
        ulash.commit()
    except (Exception, Error) as error:
        print(f"Xato1: \n\n{error}")
    finally:
        if ulash:
            cursor.close()
            ulash.close()
# createproduct()
def addCategor(name):
    try:
        ulash = connect("restaran")
        cursor = ulash.cursor()
        cursor.execute("""INSERT INTO category(name) values(?);""", (name,))
        ulash.commit()
    except (Exception, Error) as error:
        print(f"Xato1.5: \n\n{error}")
    finally:
        if ulash:
            cursor.close()
            ulash.close()
# addCategor(name='category')
def addproduct(name, narxi, rasmi, category_name):
    try:
        ulash = connect("restaran")
        cursor = ulash.cursor()
        cursor.execute("""INSERT INTO maxsulot(name, narxi, rasmi, category_name) values(?,?,?,?);""", (name, narxi, rasmi, category_name))
        ulash.commit()
    except (Exception, Error) as error:
        print(f"Xato2: \n\n{error}")
    finally:
        if ulash:
            cursor.close()
            ulash.close()

def readCategory():
    try:
        ulash = connect("maxsulotlar")
        cursor = ulash.cursor()
        cursor.execute("""Select * from kategorya""")
        a = cursor.fetchall()
        return a
    except (Exception, Error) as error:
        print(f"Xato3: \n\n{error}")
    finally:
        if ulash:
            cursor.close()
            ulash.close()

def readproduct():
    try:
        ulash = connect("restaran")
        cursor = ulash.cursor()
        cursor.execute("""Select * from maxsulot""")
        a = cursor.fetchall()
        return a
    except (Exception, Error) as error:
        print(f"Xato4: \n\n{error}")
    finally:
        if ulash:
            cursor.close()
            ulash.close()

@dp.message(CommandStart())
async def starbot(message:Message):
    if message.from_user.id == 5148276461:
        await message.answer(f"Assalomu Alaykum {message.from_user.full_name}\nsizga adminlik huquqi berilgan qo'shimcha funksiyalardan foydalanishingiz mummkin", reply_markup=admin)
    else:
        await message.answer(f"Assalomu Alaykum {message.from_user.full_name}\nNima buyurtma berasiz",reply_markup=menyu)

@dp.message(Admin.start)
async def starbot(message:Message):
    if message.from_user.id == 5148276461:
        await message.answer(f"Bosh saxifaga qaydingiz", reply_markup=admin)
    else:
        await message.answer(f"Bosh saxifaha qaydingzi",reply_markup=menyu)


@dp.message(F.text == "Orqaga 🔙")
async def orqa(message:Message):
    if F.chat_id == 5148276461:
        await message.answer("Bosh saxifaga qaytdingiz", reply_markup=admin)
    else:
        await message.answer("Bosh saxifaga qaytdingiz", reply_markup=menyu)



def forAdmin():


    def kategorya():
        @dp.message(F.text == "Kategorya qo'shish")
        async def KategoryaBot(message:Message, state:FSMContext):
            createCategory()
            await message.answer("Kategorya nomini kiriting")
            await state.set_state(Admin.kategor)


        @dp.message(Admin.kategor)
        async def kategorya2Bot(message:Message, state:FSMContext):
            xabar = message.text
            addCategor(name=xabar)
    kategorya()

    @dp.message(F.text == "Maxsulot qoshish")
    async def maxsulotBot(message:Message, state:FSMContext):
        buttom = ReplyKeyboardBuilder()
        for i in readCategory():
            buttom.button(text=f"{i[0]}")
        buttom.button(text="Orqaga 🔙")
        buttom.adjust(2)
        await message.answer("Qaysi kategoryaga qo'shmoqchisiz", reply_markup=buttom.as_markup(resize_keyboard=True, one_time_keyboard=True))
        await state.set_state(Admin.kategor)

    @dp.message(Admin.kategor)
    async def maxsulot1bot(message:Message, state:FSMContext):
        for i in readCategory():
            if i[0] == message.text:
                await state.update_data({"kategorya" : i[0]})
                await message.answer("Maxsulot nomini kiriting ")
                await state.set_state(Admin.maxsulot_qosish)

    @dp.message(Admin.maxsulot_qosish)
    async def masulot_2_bor(message:Message, state:FSMContext):
        await state.update_data({"nomi" : message.text})
        await message.answer("Narxini kiriting 💸")
        await state.set_state(Admin.maxsulot_nomi)



    @dp.message(Admin.maxsulot_nomi)
    async def masulot_3_bor(message:Message,  state:FSMContext):
        if message.text.isdigit():
            await state.update_data({"narxi" : message.text})
            await message.answer(f"Maxsulotingiz uchun rasm yuboring")
            await state.set_state(Admin.maxsulot_rasm)
        else:
            await message.answer("❗️iltimos raqam ko'rinishida yozing❗️")    



    @dp.message(Admin.maxsulot_rasm)
    async def maxsulot4Bot(message:Message, state:FSMContext):
        try:
            await message.answer_photo(photo=message.text, caption="Rasmni tasdiqlaysizmi ✅", reply_markup=tekshir)
            await state.update_data({"rasm": message.text})
            await state.set_state(Admin.maxsulot_tekshir)
        except:
            await message.answer("❗️Siz rasm yubormadiz❗️")
        

    @dp.callback_query(Admin.maxsulot_tekshir)
    async def maxsulot5Bot(call:CallbackQuery, state:FSMContext):
        xabar = call.data
        if xabar == "ha":
            data = await state.get_data()
            await call.message.answer_photo(photo=data['rasm'], caption=f"Nomi: {data['nomi']}\nNarxi: {data['narxi']} so'm\nkategoryasi: {data['kategorya']}\nTasdiqlaysozmi ✅",reply_markup=tekshir)
            await state.set_state(Admin.maxsulot_end)
        else:
            data =await state.get_data()
            data.pop('rasm', None)
            await state.update_data(data)
            await call.message.answer("Boshqa rasm yuborishingiz mumkin")

            await state.set_state(Admin.maxsulot_rasm)


    @dp.callback_query(Admin.maxsulot_end)
    async def maxsulot5bot(call:CallbackQuery, state:FSMContext):
        xabar = call.data
        if xabar == "ha":
            data = await state.get_data()
            addproduct(name=data['nomi'], narxi=data['narxi'], rasmi=data['rasm'], category_name=data['kategorya'])
            await call.message.answer("Muaffaqiyatli saqlandi")
        else:
            await state.clear()
            await state.set_state(Admin.start)


forAdmin()


def forUser():
    @dp.message(F.text == "Taom buyurtma berish")
    async def tanlov(messege:Message, state:FSMContext):
        kategorya = ReplyKeyboardBuilder()
        for i in readCategory():
            kategorya.button(text=f"{i[0]}")
        kategorya.button(text="Orqaga 🔙")
        kategorya.adjust(2)
        await messege.answer(text="fd",reply_markup=kategorya.as_markup(resize_keyboard=True, one_time_keyboard=True))
        await state.set_state(User.kategorya)

    @dp.message(User.kategorya)
    async def maxsulot(messege:Message, state:FSMContext):
        taom = ReplyKeyboardBuilder()
        for i in readproduct():
            if i[3] == messege.text:
                taom.button(text=i[0])
        taom.button(text="Orqaga 🔙")
        taom.adjust(2)
        await messege.answer("ha", reply_markup=taom.as_markup(resize_keyboard=True, one_time_keyboard=True))
forUser()

        


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print("Tugadi")
