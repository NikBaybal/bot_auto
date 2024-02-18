from aiogram_dialog import (Dialog, Window, DialogManager)
from aiogram_dialog.widgets.kbd import Next, Column, Back, Select
from aiogram_dialog.widgets.text import Const, Format, Case
from . import states
from .main import MAIN_MENU_BUTTON
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
import datetime
from aiogram.types import Message,CallbackQuery
import utils

async def get_master( dialog_manager: DialogManager,**_kwargs):
    masters=utils.masters()
    return {
         "masters": masters,
    }
async def master_selection(callback: CallbackQuery, widget: Select,
                             dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['master'] = item_id
    await dialog_manager.next()


master_window = Window(
    Const(text='Выберите инструктора:'),
    Column(
        Select(
            Format('{item}'),
            id='master',
            item_id_getter=lambda x: x,
            items='masters',
            on_click=master_selection
         ),
    ),
    MAIN_MENU_BUTTON,
    state=states.Record.Master,
    getter=get_master,
)



async def get_date( dialog_manager: DialogManager,**_kwargs):
    dates=utils.dates(dialog_manager.dialog_data.get('master'))
    return {
         "dates": dates,
    }
async def date_selection(callback: CallbackQuery, widget: Select,
                             dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['date'] = item_id
    await dialog_manager.next()


date_window = Window(
    Const(text='Выберите инструктора:'),
    Column(
        Select(
            Format('{item}'),
            id='date',
            item_id_getter=lambda x: x,
            items='dates',
            on_click=date_selection
         ),
    ),
    MAIN_MENU_BUTTON,
    state=states.Record.Date,
    getter=get_date,
)

"""
def date_check(text: str) -> str:
    if datetime.date.fromisoformat(text):
        return text
    raise ValueError("Incorrect data format, should be YYYY-MM-DD")

async def correct_date_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text:str):
    dialog_manager.dialog_data['user_input'] = text
    await dialog_manager.next()

async def error_date_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str):
    await message.answer(
        text='Вы ввели некорректную дату. Попробуйте еще раз'
    )

date_window = Window(
    Const("Выберите дату:"),
    MAIN_MENU_BUTTON,
    TextInput(
        id='date_input',
        type_factory=date_check,
        on_success=correct_date_handler,
        on_error=error_date_handler,
    ),
    state=states.Record.Date,
)


"""





async def hours_selection(callback: CallbackQuery, widget: Select,
                             dialog_manager: DialogManager, item_id: str):
    date=dialog_manager.dialog_data.get('date')
    hour=item_id
    user_name = callback.message.from_user.username
    utils.record_user(date, hour, user_name)
    await callback.message.answer(text=f'Вы успешно записались!'+'\n'f'Выбранная дата: {date}'+'\n'+f'Выбранное время: {hour}', parse_mode='HTML')


async def get_hours( dialog_manager: DialogManager,**_kwargs):
    date=dialog_manager.dialog_data.get('date')
    hours=utils.free_hours(date)
    return {
         "hours": hours,
    }


hour_window = Window(
    Const(text='Свободные часы:'),
    Column(
        Select(
            Format('{item}'),
            id='hour',
            item_id_getter=lambda x: x,
            items='hours',
            on_click=hours_selection
         ),
    ),
    Back(),
    MAIN_MENU_BUTTON,
    state=states.Record.Hour,
    getter=get_hours,
)





record_dialog = Dialog(
    master_window,
    date_window,
    hour_window,

)