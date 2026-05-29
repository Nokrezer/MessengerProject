from shared.exceptions import *

import uuid

from shared.types import ChatTypes

class MessengerService():
    def __init__(self, message_database, chat_database):
        self.message_database = message_database
        self.chat_database = chat_database

    async def _exist_chat(self, chat_id):
        exist_chat = self.chat_database.get_chat(chat_id=chat_id)

        if not exist_chat:#Если чат не найден в БД - ошибка
            raise ChatNotExist()
        
    async def _create_private_chat(self, sender_id, reader_id):
        chat_id = uuid.uuid4().hex
        
        await self.chat_database.create_chat(sender_id=sender_id,
                                            reader_id=reader_id,
                                            chat_type=ChatTypes.PRIVATE,
                                            chat_id=chat_id)
        
        return chat_id

    #sender_id - id отправителя, reader_id - отправляет клиент, id пользователя которому отправляем соо
    async def send_message(self, message, message_type, nonce, sender_id, reader_id, chat_id):
        if chat_id:#Если передан id чата
            await self._exist_chat(chat_id=chat_id)#Проверка на существование чата
            
        elif reader_id:#Если передан id пользователя(получателя)(личный чат)
            chat_id = await self.chat_database.get_chat_by_members(sender_id, reader_id)
            
            if not chat_id:#Если чата не существует, создаём
                chat_id = await self._create_private_chat(sender_id=sender_id, reader_id=reader_id)
            else:
                chat_id = chat_id.get("chat_id")

        else:
            raise NeedChatOrUserId()
        
        message_id = uuid.uuid4().hex
        await self.message_database.send_message(sender_id=sender_id, chat_id=chat_id,
                                                message=message, nonce=nonce,
                                                message_id=message_id,
                                                message_type=message_type)
    
    #Получение id чатов, в которых состоит пользователь
    async def get_user_chats(self, user_id):
        return await self.chat_database.get_user_chats(user_id)