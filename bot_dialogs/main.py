from aiogram_dialog import Dialog, Window, LaunchMode
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const,Format
from bot_dialogs import states
from aiogram.types import ContentType
import texts.start

MAIN_MENU_BUTTON = Start(
    text=Const("☰ Основное меню"),
    id="__main__",
    state=states.Main.MAIN,
)
main_dialog = Dialog(
    Window(
        Format(texts.start.start),
        Start(
            text=Const('📝 Запись'),
            id="price",
            state=states.Record.MAIN,
        ),
        Start(
            text=Const('ℹ️ О нас'),
            id="about",
            state=states.About.MAIN,
        ),
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
