from aiogram_dialog import (Dialog, Window, DialogManager)
from aiogram_dialog.widgets.kbd import Next, Column, Back, Select
from aiogram_dialog.widgets.text import Const, Format, Case
from . import states
from .main import MAIN_MENU_BUTTON
from aiogram.types import Message,CallbackQuery
import utils
from aiogram.types import User

async def get_master(**_kwargs):
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
    Const(text='Выберите дату:'),
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



async def hours_selection(callback: CallbackQuery, widget: Select,
                             dialog_manager: DialogManager, item_id: str):
    master=dialog_manager.dialog_data.get('master')
    date = dialog_manager.dialog_data.get('date')
    hour = item_id
    user_name = dialog_manager.dialog_data.get('user')
    utils.record_user(date, hour, user_name)
    await callback.message.answer(text=f'Вы успешно записались!'+'\n'f'Выбранный инструктор: {master}'+'\n'f'Выбранная дата: {date}'+'\n'+f'Выбранное время: {hour}', parse_mode='HTML')

async def get_hours( dialog_manager: DialogManager,event_from_user: User,**_kwargs):
    date=dialog_manager.dialog_data.get('date')
    dialog_manager.dialog_data['user']=event_from_user.first_name
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