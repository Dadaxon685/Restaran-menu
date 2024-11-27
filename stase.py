from aiogram.fsm.state import StatesGroup, State

class categoryrom(StatesGroup):
    nomi = State()
    finish = State()

class productform(StatesGroup):
    category_id = State()
    nomi =State()
    narxi = State()
    rasm = State()
  
    finish = State()
