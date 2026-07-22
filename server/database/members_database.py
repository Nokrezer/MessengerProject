class MembersDatabase():
    def __init__(self, database):
        self.database = database

    async def get_chat_members(self, chat_id, user_id):
        return await self.database.get_data("""SELECT user_id FROM chats_members
                                            WHERE chat_id=%s AND EXISTS(SELECT user_id FROM chats_members
                                                                        WHERE user_id=%s AND chat_id=%s)""", chat_id, user_id, chat_id, fetchall=True)