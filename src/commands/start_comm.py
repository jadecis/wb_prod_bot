from loader import db
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from src.other.other_func import filter_cat
import json

router= Router()
# https://www.wildberries.ru/catalog/{}/detail.aspx
@router.message(CommandStart())
async def start_com(msg: Message, state: FSMContext):
    await state.clear()
    sub= db.check_subscribe(msg.chat.id)
    while sub:
        user_settings= db.get_user_settings(msg.chat.id)
        sale= "> 50" if user_settings["sale"] == 51 else f"< {user_settings['sale']}"
        catalog= set(filter_cat(json.loads(user_settings['catalog'])["catalog"]))
        goods= db.get_gds(sale, catalog, user_settings["remain"])
        