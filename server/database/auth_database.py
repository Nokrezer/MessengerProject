class AuthDatabase():
    def __init__(self, database):
        self.database = database

    async def registration(self, user_id, name, salt, password_hash, email_hash):
        await self.database.create("""INSERT INTO users(user_id, name, salt, password_hash, email_hash)
                                   VALUES(%s, %s, %s, %s, %s)""", user_id, name, salt, password_hash, email_hash)
        
    async def login_by_email(self, email_hash):
        return await self.database.get_data("""SELECT * FROM users
                                            WHERE email_hash=%s""", email_hash)
    
    async def login_by_nick_name(self, nick_name):
        return await self.database.get_data("""SELECT * FROM users
                                            WHERE nick_name=%s""", nick_name
                                            )
    
