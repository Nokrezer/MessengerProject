class KeyService():
    def __init__(self, key_database, user_service):
        self.key_database = key_database
        self.user_service = user_service

    async def save_public_keys(self, user_id, public_key, pre_key, signature):
        await self.key_database.save_public_keys(user_id, public_key, pre_key, signature)

    async def get_public_keys(self, user_id=None):
        return await self.key_database.get_latest_public_keys(user_id)