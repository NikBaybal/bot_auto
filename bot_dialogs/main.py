from aiogram_dialog import Dialog, Window, LaunchMode
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const,Format
from . import states
from aiogram.types import ContentType
import texts.category

MAIN_MENU_BUTTON = Start(
    text=Const("☰ Main menu"),
    id="__main__",
    state=states.Main.MAIN,
)
main_dialog = Dialog(
    Window(
        Const("Выберите нужную кнопку:"),
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

main_window = Window(
    Format(texts.start.about_us),
    StaticMedia(path ='files/about.jpg',type = ContentType.PHOTO),
    MAIN_MENU_BUTTON,
    state=states.About.MAIN,
)

about_dialog = Dialog(
    main_window
)