import asyncio
import logging

import betterlogging as bl
from aiogram import Bot, Dispatcher, Router
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from tgbot.config import load_config
from tgbot.handlers.admin import admin_router
from tgbot.handlers.echo import echo_router
from tgbot.handlers.user import user_router
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.services import broadcaster
from aiogram.filters import Command
from aiogram.types import Message, BotCommand, BufferedInputFile, InputFile
from aiogram_dialog import DialogRegistry, Dialog, DialogManager, StartMode
from windows import Main, main_window, third_window_conv, third_window_link, forth_window_link, \
    fifth_window_link, second_window_conv, first_window_convert, first_window_download, \
    playlist_window, second_window_download, download_by_link_window, full_video_window
from run import bot


logger = logging.getLogger(__name__)
log_level = logging.INFO
bl.basic_colorized_config(level=log_level)


async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, "Бот був запущений")


def register_global_middlewares(dp: Dispatcher, config):
    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))


async def set_default_commands(dp):
    commands = [
        BotCommand(command="start", description="Запустити бота/Start the bot/Запустить бота"),
        BotCommand(command="info", description="Опис можливостей бота/Description of bot functions/Описание возможностей бота"),
        BotCommand(command="test",
                   description="test")
    ]
    await bot.set_my_commands(commands)
    await bot.set_chat_menu_button()



async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    if config.tg_bot.use_redis:
        storage = RedisStorage.from_url(config.redis.dsn(), key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True))
    else:
        storage = MemoryStorage()
    #bot = Bot(token=config.tg_bot.token, parse_mode='HTML', session=AiohttpSession(api=local_server))
    dp = Dispatcher(storage=storage)
    dialog = Dialog(main_window, first_window_convert, first_window_download, second_window_conv,
                    second_window_download,
                    third_window_conv, playlist_window, third_window_link, forth_window_link, fifth_window_link,
                    download_by_link_window, full_video_window)



    for router in [
        admin_router,
        user_router,
        echo_router
    ]:
        dp.include_router(router)

    registry = DialogRegistry(dp)
    registry.register(dialog)
    registry.setup_dp(dp)
    await set_default_commands(dp)
    register_global_middlewares(dp, config)
    await bot.delete_webhook(drop_pending_updates=True)
    await on_startup(bot, config.tg_bot.admin_ids)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот був вимкнений!")
