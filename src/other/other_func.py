
from loader import aioDB
from PIL import Image, ImageDraw, ImageFont
from config import SUB_NAME_BOT
import aiohttp
import os
import asyncio
import logging



async def create_query(rm_cat, xs, ys, value):
    res= await aioDB.get_catalog_ids()
    rm_cat.append(0)
    sqlquery=""
    for i in res:
        if i["wb_id"] not in rm_cat:
            sqlquery+=f"SELECT name, prod_id, cur_price, sale, value, date_up FROM wbProducts_db.cat{i['wb_id']}\n "\
                f"WHERE sale BETWEEN {xs} and {ys} and value >= {value}\n UNION\n"
    
    return sqlquery[:-6] if len(sqlquery) > 10 else False 


async def get_img_url(prod_id):
    
    short_id= int(prod_id) // 100000
    if 0 <= short_id <= 143:
        basket = '01'
    elif 144 <= short_id <= 287:
        basket = '02'
    elif 288 <= short_id <= 431:
        basket = '03'
    elif 432 <= short_id <= 719:
        basket = '04'
    elif 720 <= short_id <= 1007:
        basket = '05'
    elif 1008 <= short_id <= 1061:
        basket = '06'
    elif 1062 <= short_id <= 1115:
        basket = '07'
    elif 1116 <= short_id <= 1169:
        basket = '08'
    elif 1170 <= short_id <= 1313:
        basket = '09'
    elif 1314 <= short_id <= 1601:
        basket = '10'
    elif 1602 <= short_id <= 1655:
        basket = '11'
    elif 1656 <= short_id <= 1919:
        basket = '12'
    else:
        basket = '13'

    url= f"https://basket-{basket}.wbbasket.ru/vol{short_id}/part{prod_id // 1000}/{prod_id}/images/big/1.webp"
    
    return url

async def get_img(user_id, prod_id):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(await get_img_url(prod_id)) as response:
                with open(f'src/images/download/{user_id}{prod_id}.png', 'wb') as f:
                    f.write(await response.read())
        await asyncio.sleep(1)
    
        res= await watermark_img(f'{user_id}{prod_id}.png', SUB_NAME_BOT)
        return res
    except Exception as ex:
        logging.error(ex) 
        try:
            os.remove(f'src/images/download/{user_id}{prod_id}.png')
        except:
            pass
        return False
         
async def watermark_img(img_path, watermark):
    image= Image.open(f"src/images/download/{img_path}")
    image_width, image_height = image.size
    font_size = int(image_width / 8)
    font = ImageFont.truetype('src/other/3.ttf', font_size)
    x, y = int(image_width / 2), int(image_height-50)
    
    dr = ImageDraw.Draw(image)
    dr.text((x, y), watermark, font=font, fill='black', anchor="ms")
    
    image.save(f"src/images/finished/{img_path}")
    os.remove(f"src/images/download/{img_path}")
    
    return f"src/images/finished/{img_path}"
