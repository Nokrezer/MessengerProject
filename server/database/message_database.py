class MessageDatabase():
    def __init__(self, database):
        self.database = database

    async def send_message(self, sender_id, chat_id, message, nonce, message_id, message_type):
        await self.database.create("""INSERT INTO messages(nonce, sender_id, chat_id, message, message_id, message_type)
                                   VALUES(%s, %s, %s, %s, %s, %s)""", nonce, sender_id, chat_id, message, message_id, message_type)

    # async def send_message_by_user_id(self, user_id, message)