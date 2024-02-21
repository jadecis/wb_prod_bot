from loader import aioDB
from aiogram import Router
from config import SUB_NAME_BOT
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from src.messages.message import *
from src.other.other_func import create_query, get_img
import asyncio
import json
from random import randint
import os
import logging

router= Router()

@router.message(CommandStart())
async def start_com(msg: Message, state: FSMContext):
    await state.clear()
    sub= await aioDB.check_subscribe(msg.chat.id)
    if sub:
        await msg.answer(text=start_sub_msg)
        if not sub["launch"]:
            await aioDB.user_launch(msg.chat.id)
            while sub:
                user_settings= await aioDB.get_user_settings(msg.chat.id)
                if user_settings["page"] == 0:
                    page= 1 
                    await aioDB.set_page(msg.chat.id)
                else:
                    page= user_settings["page"]

                query= await create_query(json.loads(user_settings['catalog'])["catalog"], 
                                    user_settings["xs"], user_settings["ys"], 
                                    user_settings["remain"])
                if query: goods= await aioDB.get_gds(query, page)
                else: continue
                if not goods:
                    if page==1:
                        await asyncio.sleep(300)
                    page=1
                    continue
                for i in goods:
                    img_path= await get_img(msg.chat.id, int(i['prod_id']))
                    sl= (100-i["sale"]) if (100-i["sale"]) != 0 else 1
                    old_price=(i["cur_price"] / sl)
                    message= wbcard_msg.format(user_settings['name_sale'], i["sale"], i["cur_price"] // 100,
                                               int(old_price), i["name"], i["prod_id"], i["value"])
                    try:
                        await msg.answer_photo(photo=FSInputFile(img_path),
                                                caption= message)
                    except Exception as ex:
                        await msg.answer(message)    
                    try:
                        os.remove(img_path)
                    except Exception as ex:
                        logging.error(ex) 
                    await asyncio.sleep(randint(10, 30))
                await aioDB.set_page(msg.chat.id)
                sub= await aioDB.check_subscribe(msg.chat.id)
    else:
        await msg.answer(text=start_unsub_msg.format(SUB_NAME_BOT))