from shared.types import *

class ChatDatabase():
    def __init__(self, database):
        self.database = database
    
    #Получение данных о чате по его id
    async def get_chat(self, chat_id):
        return await self.database.get_data("""SELECT * FROM chats
                                            WHERE chat_id=%s""", chat_id)
    
    #Получение пользовательских чатов вместе с участниками
    async def get_user_chats(self, user_id):
        return await self.database.get_data("""
                                            SELECT chats.chat_id, chats.chat_type,
                                            COALESCE(
                                                CASE WHEN chats.chat_type = %s THEN users.name END,
                                                chats.title
                                            ) AS title,
                                            COALESCE(
                                                CASE WHEN chats.chat_type = %s THEN users.image_name END,
                                                chats.chat_image
                                            ) AS chat_image
                                            
                                            FROM chats
                                            JOIN chats_members AS ch_mem ON ch_mem.user_id = %s
                                            JOIN chats_members ON chats_members.chat_id = ch_mem.chat_id AND NOT chats_members.user_id = ch_mem.user_id
                                            JOIN users ON users.user_id = chats_members.user_id
                                            WHERE chats.chat_id = chats_members.chat_id""", 
                                            ChatTypes.PRIVATE, ChatTypes.GROUP, user_id, fetchall=True)
    
    #Функция для поиска чата, в котором уже состоят участники
    async def get_chat_by_members(self, member_id_1, member_id_2):
        return await self.database.get_data("""
                                            SELECT cm1.chat_id
                                            FROM chats_members cm1
                                            JOIN chats_members cm2 
                                            ON cm1.chat_id = cm2.chat_id
                                            JOIN chats
                                            ON cm1.chat_id = chats.chat_id
                                            WHERE cm1.user_id = %s
                                            AND cm2.user_id = %s
                                            AND chats.chat_type = %s;""", member_id_1, member_id_2, ChatTypes.PRIVATE)
    
    async def create_private_chat(self, sender_id, reader_id, chat_id):
        await self.database.create("""
                                   INSERT INTO chats(chat_id, chat_type)
                                   VALUES (%s, %s);
                                   INSERT INTO chats_members(user_id, chat_id)
                                   VALUES(%s, %s);
                                   INSERT INTO chats_members(user_id, chat_id)
                                   VALUES(%s, %s);
                                   """, chat_id, ChatTypes.PRIVATE, sender_id, chat_id, reader_id, chat_id)
    
    async def get_chat_data(self, chat_id, user_id):
        return await self.database.get_data("""SELECT chats.chat_type, chats.title,
                                            chats.created_at, JSON_ARRAYAGG(cm.user_id) AS user_ids
                                            FROM chats
                                            JOIN chats_members AS cm ON cm.chat_id = %s
                                            WHERE chats.chat_id=%s AND EXISTS(SELECT user_id FROM chats_members
                                                                                WHERE user_id = %s AND chat_id = %s)
                                            GROUP BY chats.chat_type, chats.title, chats.created_at""", chat_id, chat_id, user_id, chat_id)
    
    async def get_chat_type(self, chat_id):
        return await self.database.get_data("""SELECT chat_type FROM chats
                                            WHERE chat_id=%s""", chat_id)
    
    #метод для приватных чатов. Нужен чтобы получить id собеседника
    async def get_second_user_id(self, chat_id, user_id):
        return await self.database.get_data("""SELECT user_id FROM chats_members
                                            WHERE chat_id=%s AND NOT user_id=%s""", chat_id, user_id)

    
    async def create_group_chat(self, user_id, chat_id):
        await self.database.create("""INSERT INTO chats(chat_id, chat_type)
                                   VALUES(%s, %s);
                                   INSERT INTO chats_members(chat_id, user_id)
                                   VALUES(%s, %s)""", chat_id, ChatTypes.GROUP, chat_id, user_id)
        
    async def add_members(self, users_ids):
        values = ",".join(["(%s, %s)"] * (len(users_ids)//2))
        
        await self.database.create(f"""INSERT INTO chats_members(chat_id, user_id)
                                   VALUES {values}""", *users_ids)
        
    async def get_chat_id_by_message(self, message_id):
        return await self.database.get_data("""SELECT chat_id FROM messages
                                            WHERE message_id=%s""", message_id)