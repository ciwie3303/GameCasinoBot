from aiogram.dispatcher.filters.state import StatesGroup, State


class OtherGameState(StatesGroup):
    bet_amount = State()


class BlackjackGameState(StatesGroup):
    bet_amount = State()


class SlotsGameState(StatesGroup):
    bet_amount = State()


class AdminSearchUserState(StatesGroup):
    user_id = State()


class DepositQiwiState(StatesGroup):
    amount = State()


class BakkaraGameState(StatesGroup):
    bet_amount = State()


class OutputState(StatesGroup):
    amount = State()
    place = State()
    requesites = State()
    confirm = State()


class JackpotGameState(StatesGroup):
    bet_amount = State()


class AdminChangeBalance(StatesGroup):
    amount = State()
    confitm = State()


class AdminChangeComission(StatesGroup):
    percent = State()
    confitm = State()


class AdminPictureMailing(StatesGroup):
    text = State()
    picture = State()
    confirm = State()


class AdminWithoutPictureMailing(StatesGroup):
    text = State()
    confirm = State()