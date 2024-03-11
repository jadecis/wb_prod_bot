from aiomysql import DictCursor, Pool
from src.database.aioconnection import db_connect
import logging

class DBCommands:
    pool: Pool = db_connect
    
    async def insert(self, sql, data=()):
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor(DictCursor) as cur:
                    await cur.execute(sql, data)
                    return cur.rowcount
        except Exception as ex:
            logging.error(ex)
            return 0

    async def select_all(self, sql, data=()):
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor(DictCursor) as cur:
                    await cur.execute(sql, data)
                    return await cur.fetchall()
        except Exception as ex:
            logging.error(ex)
            return []

    async def select_one(self, sql, data=()):
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor(DictCursor) as cur:
                    await cur.execute(sql, data)
                    return await cur.fetchone()
        except Exception as ex:
            logging.error(ex)
            return {}
            
    async def check_subscribe(self, user_id):
        return await self.select_one(
            "SELECT * FROM subscribers WHERE user_id=%s", (user_id, )
        )
    
    async def check_change(self, user_id):
        return await self.select_one(
            "SELECT page FROM setting_users WHERE user_id=%s", (user_id, )
        )
    
    async def get_user_settings(self, user_id):
        return await self.select_one("""SELECT 
            setting_users.market, cat_users.cats AS catalog, remain.value AS remain, sale_users.sales AS sale, setting_users.page
            FROM setting_users
            LEFT JOIN remain ON setting_users.remaining = remain.id
            LEFT JOIN cat_users ON setting_users.user_id = cat_users.user_id
            LEFT JOIN sale_users ON setting_users.user_id = sale_users.user_id
            WHERE setting_users.user_id=%s""", (user_id, )
            )
        
    async def get_inf_sale(self, sale_ids):
        return await self.select_all(
            "SELECT xs, ys FROM sales WHERE id IN %s",
            (sale_ids, )
        )
    
    async def get_gds(self, query, page):
        try:
            N=100
            offset= (page-1)*N
            return await self.select_all(
                f"{query}\nORDER BY prod_id LIMIT %s OFFSET %s",
                    (N, offset, )
            )
        except Exception as ex: 
            logging.error(ex)  
            return False
            
    async def get_catalog_ids(self):
        return await self.select_all(f"SELECT wb_id FROM catalog")
    
    async def set_page(self, user_id):
        await self.insert(
            f"UPDATE setting_users SET page= page+1 WHERE user_id=%s",
            (user_id, )
        )
    
    async def reset_page(self, user_id):
        await self.insert(
            f"UPDATE setting_users SET page=1 WHERE user_id=%s", 
            (user_id, )
        )
    
    async def user_launch(self, user_id=None):
        if user_id:
            await self.insert(
                f"UPDATE subscribers SET launch=1 WHERE user_id=%s",
                (user_id, )
            )
        else:
            await self.insert(
                f"UPDATE subscribers SET launch=0 WHERE id > 0"
            )
