from settings.config import *

class MessageDatabase():
    def __init__(self, database):
        self.database = database

    async def send_message(self, sender_id, chat_id, text, nonce, message_id, message_type):
        await self.database.create("""INSERT INTO messages(nonce, sender_id, chat_id, text, message_id, message_type)
                                   VALUES(%s, %s, %s, %s, %s, %s)""", nonce, sender_id, chat_id, text, message_id, message_type)

    async def get_messages(self, chat_id, offset=0):
        return await self.database.get_data("""SELECT * FROM messages
                                            WHERE chat_id=%s
                                            ORDER BY created_at ASC
                                            LIMIT %s OFFSET %s
                                            """, chat_id, MAX_MESSAGES, offset, fetchall=True)
    
    #получение типа сообщения по его id
    async def get_message_type(self, message_id):
        return await self.database.get_data("""SELECT message_type FROM messages
                                            WHERE message_id = %s
                                            """, message_id)