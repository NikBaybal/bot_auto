import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ErrorEvent, ReplyKeyboardRemove
from aiogram_dialog import DialogManager, setup_dialogs, StartMode, ShowMode
from aiogram_dialog.api.exceptions import UnknownIntent
from bot_dialogs import states
from bot_dialogs.main import main_dialog, about_dialog
from bot_dialogs.record import record_dialog
from bot_dialogs.admin import admin_dialog
from config import Config, load_config
from menu import set_main_menu
import database
import texts.admin
import warnings
warnings.filterwarnings("ignore", "\nPyarrow", DeprecationWarning)

logger = logging.getLogger(__name__)
config: Config = load_config()
bot = Bot(token=config.tg_bot.token,
          parse_mode='HTML')


async def start(message: Message, dialog_manager: DialogManager):
    database.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    await dialog_manager.start(states.Main.MAIN, mode=StartMode.RESET_STACK)

async def admin(message: Message, dialog_manager: DialogManager):
    if message.from_user.id in config.tg_bot.admin_ids:
        await dialog_manager.start(states.Admin.MAIN, mode=StartMode.RESET_STACK)
    else:
        await message.answer("Вы не администратор", parse_mode="HTML", reply_markup=None)


async def on_unknown_intent(event: ErrorEvent, dialog_manager: DialogManager):
    logging.error("Restarting dialog: %s", event.exception)
    if event.update.callback_query:
        await event.update.callback_query.answer(
            "Bot process was restarted due to maintenance.\n"
            "Redirecting to main menu.",
        )
        if event.update.callback_query.message:
            try:
                await event.update.callback_query.message.delete()
            except TelegramBadRequest:
                pass  # whatever
    elif event.update.message:
        await event.update.message.answer(
            "Bot process was restarted due to maintenance.\n"
            "Redirecting to main menu.",
            reply_markup=ReplyKeyboardRemove(),
        )
    await dialog_manager.start(
        states.Main.MAIN,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )


dialog_router = Router()
dialog_router.include_routers(
    main_dialog,
    about_dialog,
    record_dialog,
    admin_dialog,
)


def setup_dp():
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.message.register(start, F.text == "/start")
    dp.message.register(admin, F.text == "/admin")
    dp.errors.register(
        on_unknown_intent,
        ExceptionTypeFilter(UnknownIntent),
    )
    dp.include_router(dialog_router)
    setup_dialogs(dp)
    return dp


async def main(bot: Bot):
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot')
    # Настраиваем кнопку Menu
    await set_main_menu(bot)
    dp = setup_dp()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main(bot))
