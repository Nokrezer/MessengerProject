class ChatDatabase():
    def __init__(self, database):
        self.database = database

    #Получение данных о чате по его id
    async def get_chat(self, chat_id):
        return await self.database.get_data("""SELECT * FROM chats
                                            WHERE chat_id=%s""", chat_id)
    
    async def get_user_chats(self, user_id):
        return await self.database.get_data("""SELECT chats.chat_id, chats.title
                                            FROM chats_members
                                            JOIN chats ON chats_members.chat_id = chats.chat_id
                                            WHERE chats_members.user_id = %s""", user_id, fetchall=True)
    
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
    
    # async def get_private_chat(self, sender_id, reader_id):
        # return await self.database.get_data("""SELCT * FROM chats WHERE""")

    # async def create_chat(self, chat_id, chat_type):
    
    # async def get_chat_by_user_id(self, user_id):
        # return await self