from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const,Format
from bot_dialogs import states
import texts.admin
import database


ADMIN_MENU_BUTTON = Start(
    text=Const("☰ Основное меню админа"),
    id="__main__",
    state=states.Admin.MAIN,
)

main_window = Window(
    Format(texts.admin.start_admin),
    Start(
        text=Const('Пользователи'),
        id="users",
        state=states.Admin.Users,
    ),
    Start(
        text=Const('Статистика'),
        id="stat",
        state=states.Admin.Stat,
    ),
    state=states.Admin.MAIN,
    )

stat_window = Window(
    Format(texts.admin.statistick(int(database.count()))),
    ADMIN_MENU_BUTTON,
    state=states.Admin.Stat,
    )

async def get_users( dialog_manager: DialogManager,**_kwargs):
    users = '''ID, UserName, Name, Block
        ➖➖➖➖➖➖➖➖➖\n'''
    users += database.show_users()
    return {"users": users}

users_window = Window(
    Format('{users}'),
    ADMIN_MENU_BUTTON,
    state=states.Admin.Users,
    getter=get_users,
    )

admin_dialog = Dialog(
    main_window,
    stat_window,
    users_window,
)