from loader import db
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
    sub= await db.check_subscribe(msg.chat.id)
    if sub:
        await msg.answer(text=start_sub_msg)
        if sub.get('launch'):
            return
        await db.user_launch(msg.chat.id)
        sub['launch']=1
        while (sub and (sub.get('launch'))):
            try:
                user_settings= await db.get_user_settings(msg.chat.id)
                if user_settings["page"] == 0:
                    page= 1 
                    await db.set_page(msg.chat.id)
                else:
                    page= user_settings["page"]

                query= await create_query(json.loads(user_settings['catalog'])["catalog"], 
                                    json.loads(user_settings['sale'])["sale"], 
                                    user_settings["remain"])
                if query: goods= await db.get_gds(query, page)
                else: continue
                if not goods:
                    if page==1:
                        await asyncio.sleep(300)
                    await db.reset_page(msg.chat.id)
                    continue
                for i in goods:
                    img_path= await get_img(msg.chat.id, int(i['prod_id']))
                    sl= (100-i["sale"]) if (100-i["sale"]) != 0 else 1
                    old_price=(i["cur_price"] / sl)
                    message= wbcard_msg.format("", i["sale"], i["cur_price"] // 100,
                                                int(old_price), i["name"], i["prod_id"], i["value"])
                    try:
                        await msg.answer_photo(photo=FSInputFile(img_path),
                                                caption= message)
                    except Exception as ex:
                        await msg.answer(message)    
                    try:
                        os.remove(img_path)
                    except Exception as ex:
                        # logging.error(ex)
                        pass 
                    await asyncio.sleep(randint(15, 40))
                    sub= await db.check_subscribe(msg.chat.id)
                    change= await db.check_change(msg.chat.id)
                    if (not sub) or not sub.get('launch') or (not change.get('page')):
                        break  
                await db.set_page(msg.chat.id)
            except Exception as ex:
                logging.error(ex)
                await asyncio.sleep(100)
    else:
        await msg.answer(text=start_unsub_msg.format(SUB_NAME_BOT))