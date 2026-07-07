class UserDatabase():
    def __init__(self, database):
        self.database = database
    
    async def get_user_by_id(self, user_id):
        return await self.database.get_data("""SELECT user_id, name, nickname, bio, image_name
                                            FROM users
                                            WHERE user_id=%s""", user_id)
    
    async def get_users(self, nickname):
        search = f"{nickname}%"
        return await self.database.get_data("""SELECT nickname, name, user_id FROM users
                                      WHERE nickname LIKE %s""", search, fetchall=True)
    
    async def get_user_by_chat_id(self, sender_id, chat_id):
        return await self.database.get_data("""SELECT user_id FROM chats_members
                                           WHERE chat_id=%s AND NOT user_id=%s""", chat_id, sender_id)
    
    async def get_user_image(self, user_id):
        return await self.database.get_data("""SELECT image_name FROM users
                                            WHERE user_id = %s""", user_id)
    
    async def set_user_image(self, user_id, image_name):
        await self.database.create("""UPDATE users
                                   SET image_name = %s
                                   WHERE user_id = %s""", image_name, user_id)
        
    async def set_user_name(self, user_id, name):
        await self.database.create("""UPDATE users
                                   SET name = %s
                                   WHERE user_id = %s""", name, user_id)
        
    async def set_user_nickname(self, user_id, nickname):
        await self.database.create("""UPDATE users
                                   SET nickname = %s
                                   WHERE user_id = %s""", nickname, user_id)
        
    async def set_user_bio(self, user_id, bio):
        await self.database.create("""UPDATE users
                                   SET bio = %s
                                   WHERE user_id = %s""", bio, user_id)
        
    async def set_user_email(self, user_id, email_hash):
        await self.database.create("""UPDATE users
                                   SET email_hash=%s
                                   WHERE user_id=%s""", email_hash, user_id)