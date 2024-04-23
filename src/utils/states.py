from aiogram.fsm.state import State, StatesGroup


class RequirementsState(StatesGroup):
    order_id = State() # data
    requirements_input = State() # data
    requirements_wait = State() 


class AdminForwardState(StatesGroup):
    message_id = State() # data 
    wait_message = State()
    confirm = State()