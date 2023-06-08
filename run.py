import os

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from dotenv import load_dotenv, find_dotenv

from tgbot.config import load_config

load_dotenv(find_dotenv())

#token = os.getenv('TOKEN2')
api_key = os.getenv('API_KEY')
organization = os.getenv('ORG')
#bot = Bot(token, parse_mode="HTML")

config = load_config(".env")
token = os.getenv('TOKEN')
local_server = TelegramAPIServer.from_base("http://api:8081")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML', session=AiohttpSession(api=local_server))
db_link = os.getenv('LINK')