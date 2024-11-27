from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from sqlite3 import connect, Error
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "7861852078:AAHm-gh1EXQzl-ed4mzkpzjSwr1m0zOLTfM"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()






class AdminStates(StatesGroup):
    kategoriya_qoshish = State()
    mahsulot_kategoriya = State()
    kategoriya_korish = State()
    mahsulot_korish =   State()

    mahsulot_nomi = State()
    mahsulot_narxi = State()
    mahsulot_rasmi = State()
    mahsulot_tasdiq = State()
    reklama_malumoti = State()  


class UserStates(StatesGroup):
    kategoriya_tanlash = State()
    mahsulot_tanlash = State()
    mahsulot_soni = State()

def read_kategoriya():
    try:
        ulash = connect("restoran.db")
        cursor = ulash.cursor()
        cursor.execute("SELECT name FROM category")
        return cursor.fetchall()
    finally:
        if ulash:
            ulash.close()

def kategoriyadagi_mahsulotlarni_olish(kategoriya_nom):
    try:
        ulash = connect("restoran.db")
        cursor = ulash.cursor()
        cursor.execute("SELECT * FROM kategoriya", (kategoriya_nom,))
        return cursor.fetchall()
    finally:
        if ulash:
            ulash.close()


def mahsulotni_topish(mahsulot_nom, kategoriya_nom):
    try:
        ulash = connect("restoran.db")
        cursor = ulash.cursor()
        cursor.execute(
            "SELECT * FROM maxsulot",
            (mahsulot_nom, kategoriya_nom)
        )
        return cursor.fetchall()
    finally:
        if ulash:
            ulash.close()

def bazani_yaratish():
    try:
        conn = connect("restoran.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS kategoriya (
                nom TEXT PRIMARY KEY NOT NULL
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mahsulot (
                nom TEXT PRIMARY KEY NOT NULL,
                narx INTEGER NOT NULL,
                rasm TEXT NOT NULL,
                kategoriya_nom TEXT NOT NULL,
                FOREIGN KEY (kategoriya_nom) REFERENCES kategoriya (nom)
            );
        """)
        conn.commit()
    except Error as e:
        print(f"Bazani yaratishda xatolik: {e}")
    finally:
        conn.close()

def kategoriya_qoshish(nom):
    try:
        conn = connect("restoran.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO kategoriya (nom) VALUES (?);", (nom,))
        conn.commit()
    except Error as e:
        print(f"Kategoriyani qo'shishda xatolik: {e}")
    finally:
        conn.close()

def mahsulot_qoshish(nom, narx, rasm, kategoriya_nom):
    try:
        conn = connect("restoran.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO mahsulot (nom, narx, rasm, kategoriya_nom) VALUES (?, ?, ?, ?);",
            (nom, narx, rasm, kategoriya_nom)
        )
        conn.commit()
    except Error as e:
        print(f"Mahsulotni qo'shishda xatolik: {e}")
    finally:
        conn.close()

def kategoriyalarni_olish():
    try:
        conn = connect("restoran.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM kategoriya;")
        return cursor.fetchall()
    except Error as e:
        print(f"Kategoriyalarni olishda xatolik: {e}")
        return []
    finally:
        conn.close()


def user_baza():
    try:
        conn = connect("restoran.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                full_name TEXT
            );
        """)

        conn.commit()
    except Error as e:
        print(f"Foydalanuvchi ma'lumotlarini bazani yaratishda xatolik: {e}")
    finally:
        conn.close()
# user_baza()

def add_user_to_db(user_id, username, full_name):
    try:
        conn = connect("restoran.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO users (user_id, username, full_name)
            VALUES (?, ?, ?);
        """, (user_id, username, full_name))
        conn.commit()
    except Error as e:
        print(f"Error adding user: {e}")
    finally:
        conn.close()

def add_user(user_id, username, fullname):
    try:
        conn = connect('reklama.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO odamlar (user_id, username, fullname)
            VALUES (?, ?, ?)
        """, (user_id, username, fullname))
        conn.commit()
    except Exception as e:
        logging.error(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def fetch_users():
    try:
        conn = connect('reklama.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM odamlar")
        users = cursor.fetchall()
        return [user[0] for user in users] 
    except Exception as e:
        logging.error(f"Database error: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def readrek():
    try:
        conn = connect('reklama.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username FROM odamlar")  
        users = cursor.fetchall()
        return users  
    except Exception as e:
        logging.error(f" error: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Kategoriyani qo'shish"), KeyboardButton(text="Mahsulot qo'shish")],
            [KeyboardButton(text="Reklama berish"), KeyboardButton(text="Bosh menyu")]
        ],
        resize_keyboard=True
    )

def add_user(user_id, username, fullname):
    try:
        conn = connect('reklama.db')
        cursor = conn.cursor()

       
        cursor.execute("SELECT user_id FROM odamlar WHERE user_id = ?", (user_id,))
        existing_user = cursor.fetchone()

        if existing_user:
            logging.info(f"User {user_id} already exists in the database. Skipping...")
            return 
   
        
        cursor.execute("""
            INSERT INTO odamlar (user_id, username, fullname)
            VALUES (?, ?, ?)
        """, (user_id, username, fullname))
        conn.commit()
        logging.info(f"User {user_id} add database")
    except Exception as e:
        logging.error(f"Database error: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

@dp.message(CommandStart())
async def bot_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    fullname = message.from_user.full_name

    admin_id = 5148276461
    if user_id == admin_id:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Kategoriyani qo'shish"), KeyboardButton(text="Mahsulot qo'shish")],
                [KeyboardButton(text="Reklama berish"), KeyboardButton(text="Userlar")]
            ],
            resize_keyboard=True
        )
        await message.answer("Xush kelibsiz, admin! Nima qilmoqchisiz?", reply_markup=keyboard)
    else:
        await message.answer("Xush kelibsiz! Buyurtma qilish uchun kategoriyani tanlang.", reply_markup=foydalanuvchi_menyu())
    
    add_user(user_id=user_id, username=username, fullname=fullname)



@dp.message(F.text == "Reklama berish")
async def reklama_post(message: Message):
    users = fetch_users()
    
    if not users:
        await message.answer("Hali hech qanday foydalanuvchi yo'q.")
        return

    await message.answer(f"{len(users)} foydalanuvchiga reklama yuborilmoqda...")

    sent_count = 0
    failed_count = 0

    for user_id in users:
        try:
            await bot.send_photo(
                chat_id=user_id,
                photo="https://avatars.mds.yandex.net/i?id=e434c4fb21627abf90a526c71658f143eb36ecda5bf46a30-11932700-images-thumbs&n=13",
                caption="Pytonchilar qanisizlar  👀"
            )
            sent_count += 1
        except Exception as e:
            logging.error(f"Failed to send photo to {user_id}: {e}")
            failed_count += 1

    await message.answer(
        f"Reklama yuborildi.\n"
        f"✅ Yuborilganlar: {sent_count}\n"
        f"❌ Yuborilmaganlar: {failed_count}"
    )

@dp.message(F.text == 'Userlar')
async def userlar_boshlash(message: Message, state: FSMContext):
    users = readrek()  
    for i in users:  
        await message.answer(f"User id: {i[0]}\n\n Username: {i[1]}")

def foydalanuvchi_menyu():
    builder = ReplyKeyboardBuilder()
    kategoriyalar = kategoriyalarni_olish()
    for kategoriya in kategoriyalar:
        builder.button(text=kategoriya[0])
    builder.button(text="Orqaga")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

@dp.message(F.text == "Kategoriyani qo'shish")
async def kategoriya_qoshish_boshlash(message: Message, state: FSMContext):
    await message.answer("Kategoriyaning nomini kiriting:")
    await state.set_state(AdminStates.kategoriya_qoshish)

@dp.message(AdminStates.kategoriya_qoshish)
async def kategoriya_saqlash(message: Message, state: FSMContext):
    kategoriya_qoshish(message.text)
    await message.answer(f"Kategoriya '{message.text}' muvaffaqiyatli qo'shildi.")
    await state.clear()

@dp.message(F.text == "Mahsulot qo'shish")
async def mahsulot_qoshish_boshlash(message: Message, state: FSMContext):
    kategoriyalar = kategoriyalarni_olish()
    if not kategoriyalar:
        await message.answer("Avval kamida bitta kategoriyani qo'shing.")
        return

    builder = ReplyKeyboardBuilder()
    for kategoriya in kategoriyalar:
        builder.button(text=kategoriya[0])
    builder.adjust(2)
    await message.answer("Mahsulot uchun kategoriyani tanlang:", reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(AdminStates.mahsulot_kategoriya)

@dp.message(AdminStates.mahsulot_kategoriya)
async def mahsulot_kategoriya_saqlash(message: Message, state: FSMContext):
    await state.update_data(kategoriya=message.text)
    await message.answer("Mahsulot nomini kiriting:")
    await state.set_state(AdminStates.mahsulot_nomi)

@dp.message(AdminStates.mahsulot_nomi)
async def mahsulot_nomi_saqlash(message: Message, state: FSMContext):
    await state.update_data(nom=message.text)
    await message.answer("Mahsulot narxini kiriting:")
    await state.set_state(AdminStates.mahsulot_narxi)

@dp.message(AdminStates.mahsulot_narxi)
async def mahsulot_narxi_saqlash(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Iltimos, to'g'ri narxni kiriting.")
        return

    await state.update_data(narx=int(message.text))
    await message.answer("Mahsulot uchun rasm URL manzilini yuboring:")
    await state.set_state(AdminStates.mahsulot_rasmi)

@dp.message(AdminStates.mahsulot_rasmi)
async def mahsulot_rasmi_saqlash(message: Message, state: FSMContext):
    await state.update_data(rasm=message.text)
    data = await state.get_data()

    await message.answer(
        f"Mahsulot: {data['nom']}\nNarx: {data['narx']} so'm\nKategoriya: {data['kategoriya']}\n"
        f"Tasdiqlaysizmi?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Tasdiqlash"), KeyboardButton(text="Bekor qilish")]
            ],
            resize_keyboard=True
        )
    )
    await state.set_state(AdminStates.mahsulot_tasdiq)

from butom import keybord
@dp.message(AdminStates.mahsulot_tasdiq, F.text == "Tasdiqlash")
async def mahsulot_tasdiqlash(message: Message, state: FSMContext):
    data = await state.get_data()
    mahsulot_qoshish(data['nom'], data['narx'], data['rasm'], data['kategoriya'])
    await message.answer("Mahsulot muvaffaqiyatli qo'shildi.",reply_markup=keybord)
    await state.clear()

@dp.message(AdminStates.mahsulot_korish, F.text == 'Bekor qilish')
async def mahsulot_bekor_qilish(message: Message, state: FSMContext):
   
    await message.answer("Mahsulot qayta tanlandi.", reply_markup=keybord)
    await state.clear()

@dp.message(F.text == 'Userlar')
async def userlar_boshlash(message: Message, state: FSMContext):
    users = readrek()  
    for i in users:  
        await message.answer(f"User id: {i[0]}\n\n Username: {i[1]}")


        

@dp.message(F.text == "Taom buyurtma berish")
async def kategoriya_tanlash(message: Message, state: FSMContext):
    kategoriyalar = read_kategoriya() 
    
    if kategoriyalar:
        kategoriya_tugmalar = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=k[0])] for k in kategoriyalar] + [[KeyboardButton(text="Orqaga")]],
            resize_keyboard=True
        )
        await message.answer("Kategoriya tanlang:", reply_markup=kategoriya_tugmalar)
        await state.set_state(UserStates.kategoriya_tanlash)
    else:
        await message.answer("❗️ Hozircha kategoriyalar mavjud emas.")


@dp.message(UserStates.kategoriya_tanlash)
async def mahsulot_tanlash(message: Message, state: FSMContext):
    kategoriya = message.text
    mahsulotlar = kategoriyadagi_mahsulotlarni_olish(kategoriya)  
    
    if mahsulotlar:
        
        mahsulot_tugmalar = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text = m[0])] for m in mahsulotlar] + [[KeyboardButton(text="Orqaga")]],
            resize_keyboard=True
        )
        await message.answer(f"«{kategoriya}» kategoriyasidagi mahsulotlar:", reply_markup=mahsulot_tugmalar)
        await state.update_data(kategoriya=kategoriya)  
        await state.set_state(UserStates.mahsulot_tanlash)
    else:
        await message.answer(f"❗️ «{kategoriya}» kategoriyasida mahsulotlar mavjud emas.")
        await state.clear()


@dp.message(UserStates.mahsulot_tanlash)
async def buyurtma_qilish(message: Message, state: FSMContext):
    mahsulot = message.text
    data = await state.get_data()
    kategoriya = data.get("kategoriya")
    
   
    mahsulot_data = mahsulotni_topish(mahsulot, kategoriya)
    if mahsulot_data:
        nomi, narxi = mahsulot_data
        await message.answer(f"Siz «{nomi}» tanladingiz. Narxi: {narxi} so'm.\nBuyurtmani tasdiqlaysizmi?")
        await state.clear()
    else:
        await message.answer("❗️ Bunday mahsulot topilmadi. Iltimos, qayta tanlang.")

@dp.message(F.text == "Orqaga")
async def foydalanuvchi_orqaga(message: Message):
    await message.answer("Bosh menyuga qayting.", reply_markup=foydalanuvchi_menyu())

async def main():
    bazani_yaratish()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
