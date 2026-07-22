from settings.config import *

class MessageDatabase():
    def __init__(self, database):
        self.database = database

    async def send_message(self, sender_id, chat_id, text, nonce, message_id, message_type, key_version):
        await self.database.create("""INSERT INTO messages(nonce, sender_id, chat_id, text, 
                                   message_id, message_type, key_version)
                                   VALUES(%s, %s, %s, %s, %s, %s, %s)""", 
                                   nonce, sender_id, chat_id, 
                                   text, message_id, message_type, key_version)

    async def get_messages(self, chat_id, user_id, offset=0):
        return await self.database.get_data("""SELECT msg.sender_id, msg.text, msg.nonce, msg.message_type, msg.key_version,
                                                msg.message_id, msg.created_at
                                                FROM chats_members
                                                JOIN messages AS msg ON chats_members.chat_id = %s AND chats_members.user_id = %s     
                                                WHERE msg.chat_id= %s
                                                ORDER BY created_at ASC
                                                LIMIT %s OFFSET %s
                                            """, chat_id, user_id, chat_id, MAX_MESSAGES, offset, fetchall=True)
    
    #получение типа сообщения по его id
    async def get_message_type(self, user_id, message_id):
        return await self.database.get_data("""SELECT message_type FROM messages
                                                WHERE message_id = %s AND EXISTS(SELECT messages.chat_id FROM messages
                                                JOIN chats_members ON user_id = %s
                                                WHERE chats_members.chat_id = messages.chat_id AND messages.message_id = %s)
                                            """, message_id, user_id, message_id)
    
    async def delete_message(self, message_id, user_id):
        await self.database.create("""DELETE FROM messages
                                   WHERE message_id=%s AND sender_id=%s""", message_id, user_id)
        
    async def edit_message(self, user_id, message_id, nonce, text):
        await self.database.create("""UPDATE messages
                                   SET text=%s, nonce=%s
                                   WHERE message_id=%s AND sender_id=%s""", text, nonce, message_id, user_id)