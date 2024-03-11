from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from src.database.aiodb import DBCommands
# from src.database.db import Database
from config import *
import logging




bot= Bot(TOKEN_BOT, parse_mode=ParseMode.HTML)
# logging.basicConfig(level=logging.ERROR, filename="errors.log",filemode="w")
logging.basicConfig(level=logging.INFO)
dp= Dispatcher()
db = DBCommands()