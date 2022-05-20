from aiogram.dispatcher.filters.state import StatesGroup, State


class FilenameEnterState(StatesGroup):
    ENTER_FILENAME = State()