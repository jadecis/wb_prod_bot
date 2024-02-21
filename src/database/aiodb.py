from aiomysql import DictCursor, Pool
from src.database.aioconnection import db_connect
import logging

class DBCommands:
    pool: Pool = db_connect
    
    async def insert(self, sql, data=()):
        async with self.pool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                await cur.execute(sql, data)

    async def select_all(self, sql, data=()):
        async with self.pool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                await cur.execute(sql, data)
                return await cur.fetchall()

    async def select_one(self, sql, data=()):
        async with self.pool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                await cur.execute(sql, data)
                return await cur.fetchone()
            
    async def check_subscribe(self, user_id):
        return await self.select_one(
            "SELECT * FROM subscribers WHERE user_id=%s", (user_id, )
        )
        
    async def get_user_settings(self, user_id):
        return await self.select_one("""SELECT 
            sales.name AS name_sale, setting_users.market, setting_users.catalog, remain.value AS remain, sales.xs, sales.ys, setting_users.page
            FROM setting_users
            LEFT JOIN sales ON setting_users.size_sale = sales.id
            LEFT JOIN remain ON setting_users.remaining = remain.id
            WHERE user_id=%s""", (user_id, )
            )
        
    async def get_gds(self, query, page):
        try:
            N=10
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
            f"UPDATE setting_users SET page=page+1 WHERE user_id=%s", 
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
