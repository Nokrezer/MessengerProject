class MembersDatabase():
    def __init__(self, database):
        self.database = database

    async def get_chat_members(self, chat_id):
        return await self.database.get_data("""SELECT user_id FROM chats_members
                                            WHERE chat_id=%s""", chat_id, fetchall=True)