class AuthDatabase():
    def __init__(self, database):
        self.database = database

    async def registration(self, user_id, name, salt, password_hash, email_hash):
        await self.database.create("""INSERT INTO users(user_id, name, salt, password_hash, email_hash)
                                   VALUES(%s, %s, %s, %s, %s)""", user_id, name, salt, password_hash, email_hash)
        
    async def login_by_email(self, email_hash):
        return await self.database.get_data("""SELECT * FROM users
                                            WHERE email_hash=%s""", email_hash)
    
    async def login_by_nickname(self, nickname):
        return await self.database.get_data("""SELECT * FROM users
                                            WHERE nickname=%s""", nickname
                                            )
    
    async def get_user_code(self, code, user_id=None, email_hash=None):
        return await self.database.get_data("""SELECT * FROM auth_codes
                                            WHERE (user_id=%s OR email_hash=%s)
                                            AND revoked=0 AND code=%s""", user_id, email_hash, code)
    
    async def revoke_code(self, code, user_id=None, email_hash=None):
        await self.database.create("""UPDATE auth_codes
                                   SET revoked=1
                                   WHERE (user_id=%s OR email_hash=%s) AND code=%s""", user_id, email_hash, code)
        
    async def add_auth_code(self, user_id, code):
        await self.database.create("""INSERT INTO auth_codes (user_id, code)
                                    SELECT user_id, %s
                                    FROM users
                                    WHERE user_id=%s""", code, user_id)
        
    async def add_reg_code(self, email_hash, code):
        await self.database.create("""INSERT INTO auth_codes (email_hash, code)
                                    VALUES(%s, %s)""", email_hash, code)
        
    