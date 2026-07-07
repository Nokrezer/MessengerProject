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
                                            CASE
                                                WHEN chats.chat_type = "private" THEN users.name
                                                WHEN chats.chat_type = "group" THEN chats.title
                                            END AS title,
                                            CASE
                                                WHEN chats.chat_type = "private" THEN users.image_name
                                                WHEN chats.chat_type = "group" THEN chats.chat_image
                                            END AS chat_image
                                            
                                            FROM chats_members
                                            JOIN chats ON chats_members.chat_id = chats.chat_id
                                            LEFT JOIN users ON users.user_id = chats_members.user_id
                                            WHERE chats_members.chat_id = chats.chat_id AND NOT chats_members.user_id = %s""", user_id, fetchall=True)
    
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
                                            AND chats.chat_type = 'private';""", member_id_1, member_id_2)
    
    async def create_chat(self, sender_id, reader_id, chat_id, chat_type):
        await self.database.create("""
                                   INSERT INTO chats(chat_id, chat_type)
                                   VALUES (%s, %s);
                                   INSERT INTO chats_members(user_id, chat_id)
                                   VALUES(%s, %s);
                                   INSERT INTO chats_members(user_id, chat_id)
                                   VALUES(%s, %s);
                                   """, chat_id, chat_type, sender_id, chat_id, reader_id, chat_id)
    
    async def get_chat_data(self, chat_id):
        return await self.database.get_data("""SELECT chats.chat_type, chats.title,
                                            chats.created_at, JSON_ARRAYAGG(cm.user_id) AS user_ids
                                            FROM chats
                                            JOIN chats_members AS cm ON cm.chat_id = %s
                                            WHERE chats.chat_id=%s
                                            GROUP BY chats.chat_type, chats.title, chats.created_at""", chat_id, chat_id)
    
    async def get_chat_type(self, chat_id):
        return await self.database.get_data("""SELECT chat_type FROM chats
                                            WHERE chat_id=%s""", chat_id)
    
    #метод для приватных чатов. Нужен чтобы получить id собеседника
    async def get_second_user_id(self, chat_id, user_id):
        return await self.database.get_data("""SELECT user_id FROM chats_members
                                            WHERE chat_id=%s AND NOT user_id=%s""", chat_id, user_id)
    
    #проверяет, состоит ли пользователь в том чате где есть сообщение
    async def check_user_access_to_message(self, user_id, message_id):
        return await self.database.get_data("""
                                            SELECT messages.chat_id FROM messages
                                            JOIN chats_members ON user_id = %s
                                            WHERE chats_members.chat_id = messages.chat_id AND messages.message_id = %s""", user_id, message_id)
    
    async def check_user_access_to_chat(self, user_id, chat_id):
        return await self.database.get_data("""SELECT chat_id FROM chats_members
                                       WHERE chat_id = %s AND user_id = %s""", chat_id, user_id)