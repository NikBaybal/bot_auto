from aiogram_dialog import Dialog, Window, LaunchMode,DialogManager
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const,Format, Multi
from bot_dialogs import states
from aiogram.types import ContentType
import texts.start
from aiogram.types import User

MAIN_MENU_BUTTON = Start(
    text=Const("☰ Основное меню"),
    id="__main__",
    state=states.Main.MAIN,
)

async def get_name(event_from_user: User,dialog_manager:DialogManager, **kwargs):
    return {'name': event_from_user.first_name or 'Странник'}


main_dialog = Dialog(
    Window(
        Multi(
            Format('<b>Добро пожаловать,{name}, в нашу автошколу!</b>'),
            Const('В этом боте вы можете записаться к инструктору по вождению.'),
            sep='\n'
        ),
        Start(
            text=Const('📝 Запись'),
            id="price",
            state=states.Record.Master,
        ),
        Start(
            text=Const('ℹ️ О нас'),
            id="about",
            state=states.About.MAIN,
        ),
        getter=get_name,
        state=states.Main.MAIN,
    ),
    launch_mode=LaunchMode.ROOT,
)

about_dialog = Dialog(
    Window(
        Format(texts.start.about_us),
        StaticMedia(path ='files/about.jpg', type = ContentType.PHOTO),
        MAIN_MENU_BUTTON,
        state=states.About.MAIN,
    )
)
