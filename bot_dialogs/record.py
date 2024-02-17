from aiogram_dialog import (Dialog, Window, DialogManager)
from aiogram_dialog.widgets.kbd import Next, Column, Back, Select
from aiogram_dialog.widgets.text import Const, Format, Case
from . import states
from .main import MAIN_MENU_BUTTON
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
import datetime
from aiogram.types import Message,CallbackQuery
import utils

async def date_check(text: str) -> str:
    if datetime.date.fromisoformat(text):
        return text
    raise ValueError("Вы ввели некорректную дату. Попробуйте в формате \"ДД.ММ\". Например, чтобы выбрать 1 февраля написать 01.02")

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

main_window = Window(
    Const("Введите желаемую дату в формате \"ДД.ММ\". Например, чтобы выбрать 1 февраля написать 01.02:"),
    MAIN_MENU_BUTTON,
    TextInput(
        id='date_input',
        type_factory=date_check,
        on_success=correct_date_handler,
        on_error=error_date_handler,
    ),
    state=states.Record.MAIN,
)
async def hours_selection(callback: CallbackQuery, widget: Select,
                             dialog_manager: DialogManager, item_id: str):
    date=dialog_manager.dialog_data.get('user_input')
    hour=item_id
    user_name = callback.message.from_user.username
    utils.record_user(date, hour, user_name)
    await callback.message.answer(text=f'Вы успешно записались!!!!'+'\n'f'Выбранная дата: {date}'+'\n'+f'Выбранное время: {hour}', parse_mode='HTML')


async def get_hours( dialog_manager: DialogManager,**_kwargs):
    date=dialog_manager.dialog_data.get('user_input')
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
    Back('Назад'),
    MAIN_MENU_BUTTON,
    state=states.Record.Hour,
    getter=get_hours,
)

record_dialog = Dialog(
    main_window,
    hour_window,

)