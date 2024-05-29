from aiogram.dispatcher.filters.state import StatesGroup, State


class LevelState(StatesGroup):
    question = State()
    answer = State()
