from aiogram.fsm.state import State, StatesGroup


class RequirementsState(StatesGroup):
    order_id = State()
    requirements_input = State()
    requirements_wait = State() 