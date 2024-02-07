from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from src.database.db import Database
from config import *
import logging


bot= Bot(TOKEN_BOT, parse_mode=ParseMode.HTML)
logging.basicConfig(level=logging.INFO)
dp= Dispatcher()
db= Database(
    host=HOST_DB,
    port=PORT_DB,
    password=PASS_DB,
    name=NAME_DB,
    user=USER_DB
)