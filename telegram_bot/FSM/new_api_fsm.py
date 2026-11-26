from aiogram.fsm.state import StatesGroup, State

class adding_api_state(StatesGroup):
    url = State()
    send_method = State()
    body = State()
    max_delay_seconds = State()
    confirming = State()
    