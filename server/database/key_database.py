class KeyDatabase():
    def __init__(self, database):
        self.database = database

    async def save_public_keys(self, user_id, public_key, pre_key, signature):
        await self.database.create("""INSERT INTO public_keys(user_id, public_key, pre_key, signature)
                                    VALUES(%s, %s, %s, %s)""", user_id, public_key, pre_key, signature)
    
    async def get_latest_public_keys(self, user_id):
        return await self.database.get_data("""SELECT public_key, pre_key, signature
                                            FROM public_keys
                                            WHERE user_id=%s
                                            ORDER BY created_at DESC""", user_id)

    # async def get_public_keys(self, user_id):
    #     return await self.database.get_data("""SELECT public_key, pre_key, signature
    #                                         FROM public_keys
    #                                         WHERE user_id=%s
    #                                         ORDER BY created_at""", user_id, fetchall=True)
