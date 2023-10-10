from aiogram.fsm.state import StatesGroup
from aiogram.fsm.state import State


class BeginStates(StatesGroup):
    selecting_action = State()
    selecting_city = State()
    selecting_price = State()
    selecting_platform = State()


class ResultStates(StatesGroup):
    result_average_price = State()
    result_average_comparing = State()
    result_apartment_article = State()
