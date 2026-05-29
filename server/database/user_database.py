class UserDatabase():
    def __init__(self, database):
        self.database = database
    
    #Метод для поиска пользователя по хэшу почты    
    async def get_user_by_email_hash(self, email_hash):
        return await self.database.get_data("""SELECT * FROM users
                                     WHERE email_hash = %s""", email_hash)
    
    async def get_user_by_id(self, user_id):
        return await self.database.get_data("""SELECT user_id, name, nick_name, bio
                                            FROM users
                                            WHERE user_id=%s""", user_id)