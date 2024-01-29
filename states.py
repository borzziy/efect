from aiogram.dispatcher.filters.state import State, StatesGroup


class UsersStates(StatesGroup):
    get_image = State()
