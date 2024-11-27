bot_token ='7861852078:AAHm-gh1EXQzl-ed4mzkpzjSwr1m0zOLTfM'

admins =[5148276461]

###
from aiogram.fsm.state import StatesGroup, State
# token = "7872799380:AAHYOCwqbfCetw0Kzjh-TXwT4ez_KIeqG84"


class Admin(StatesGroup):
    start = State()    
    kategor = State()
    maxsulot_qosish = State()
    maxsulot_nomi = State()
    maxsulot_rasm = State()
    maxsulot_tekshir = State()
    maxsulot_end = State()

class User(StatesGroup):
    kategorya = State()
    maxsulot = State()
