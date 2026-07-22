class KeyDatabase():
    def __init__(self, database):
        self.database = database

    async def save_public_keys(self, user_id, public_key, pre_key, signature):
        return await self.database.get_data("""
                                    INSERT INTO public_keys(user_id, public_key, pre_key, signature, key_version)
                                    VALUES(%s, %s, %s, %s, COALESCE((SELECT key_version
                                                                            FROM public_keys
                                                                            WHERE user_id=%s
                                                                            ORDER BY created_at DESC LIMIT 1)+1, 1))
                                    RETURNING key_version""", user_id, public_key, pre_key, signature, user_id)
    
    async def get_latest_public_keys(self, user_id):
        return await self.database.get_data("""SELECT public_key, pre_key, signature, key_version
                                            FROM public_keys
                                            WHERE user_id=%s
                                            ORDER BY created_at DESC""", user_id)
    
    async def get_keys_by_version(self, user_id, version):
        return await self.database.get_data("""SELECT public_key, pre_key, signature
                                            FROM public_keys
                                            WHERE user_id=%s AND key_version=%s""", user_id, version)
