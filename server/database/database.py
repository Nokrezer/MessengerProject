import asyncio
import aiomysql

from settings.config import *


#Общие методы для получения/добавления/удаления/изменения данных и создания единого подключения к базе данных
class Database():
    def __init__(self):
        self.database_connection = None

    async def init(self):
        self.database_connection = await aiomysql.create_pool(host=SQL_HOST, port=SQL_PORT,
                                    user=SQL_USER, password=SQL_PASSWORD,
                                    db=SQL_DATABASE, autocommit=True)
    
    async def create(self, command, *args):#Общий метод для создания или добавление данных в БД
        async with self.database_connection.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(command, args)
                    await conn.commit()
                except Exception as e:
                    await conn.rollback()
                    raise e

    async def get_data(self, command, *args, fetchall=False):#Общий метод, для получения любых данных с БД
        async with self.database_connection.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(command, args)
                
                if fetchall:
                    return await cur.fetchall()

                return await cur.fetchone()