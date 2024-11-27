import logging
import asyncio
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Dispatcher, Bot, F
from aiogram.filters import CommandStart
from sqlite3 import connect, Error
from aiogram.fsm.storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

# Bot token
bot_token = '7936084722:AAGp0PZu4f_zqM3sMrs-H_X8MdvHShc5Lmo'

# Initialize bot and dispatcher
bot = Bot(token=bot_token)
dp = Dispatcher(storage=MemoryStorage())


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


def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Kategoriyani qo‘shish"), KeyboardButton(text="Mahsulot qo‘shish")],
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
        logging.error(f"error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



@dp.message(CommandStart())
async def bot_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    fullname = message.from_user.full_name


    add_user(user_id=user_id, username=username, fullname=fullname)


    await message.answer("Xush kelibsiz, admin! Nima qilmoqchisiz?", reply_markup=get_main_keyboard())


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
                caption="Python p 18 guruhidan reklama"
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

async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")

if __name__ == '__main__':
    asyncio.run(main())
