from aiogram.fsm.state import State, StatesGroup

class Main(StatesGroup):
    MAIN = State()
class About(StatesGroup):
    MAIN = State()

class Record(StatesGroup):
    Master = State()
    Date = State()
    Hour = State()
class Admin(StatesGroup):
    MAIN = State()
    Stat = State()
    Users = State()
