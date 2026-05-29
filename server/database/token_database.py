class TokenDatabase():
    def __init__(self, database):
        self.database = database

    async def add_refresh_token(self, token_id, user_id):
        await self.database.create("""INSERT INTO refresh_tokens (jti, user_id)
                                   VALUES (%s, %s)""", token_id, user_id)
        
    async def get_refresh_token(self, jti):#jti = token id
        return await self.database.get_data("""SELECT * FROM refresh_tokens
                                      WHERE jti=%s AND revoked=0""", jti)