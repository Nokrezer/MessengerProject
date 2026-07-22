from shared.exceptions import *

import uuid

from shared.types import *

class MessengerService():
    def __init__(self, message_database, messenger_realtime_service, file_storage_service, chat_database):
        self.message_database = message_database
        self.messenger_realtime_service = messenger_realtime_service
        self.file_storage_service = file_storage_service
        self.chat_database = chat_database
        
    #sender_id - id отправителя, reader_id - отправляет клиент, id пользователя которому отправляем соо
    #data - если передано любое медиа
    async def send_message(self, text, message_type, nonce, sender_id, reader_id, chat_id, data, key_version):
        if reader_id:#Если передан id пользователя(получателя)(личный чат)
            chat_id = await self.chat_database.get_chat_by_members(sender_id, reader_id)

        elif not chat_id:
            raise NeedChatOrUserId()
        
        message_id = uuid.uuid4().hex
        #отправляем соо в режиме реального времени(если пользователи онлайн)
        await self.messenger_realtime_service.send_message(chat_id, text, nonce, message_id, message_type, sender_id)
        
        await self.message_database.send_message(sender_id=sender_id, chat_id=chat_id,
                                                text=text, nonce=nonce,
                                                message_id=message_id,
                                                message_type=message_type,
                                                key_version=key_version)#сохраняем сообщение в бд
        
        #Проверяем типы сообщений, если тип не текст, тогда сохраняем отправленный файл
        match message_type:
            case MessageTypes.VOICE:
                await self.file_storage_service.save_voice_message(data, message_id)
    
    #Получение истории сообщений
    async def get_messages(self, user_id, chat_id, offset=0):
        messages = await self.message_database.get_messages(chat_id, user_id, offset)
        if not messages:#если none - либо нет сообщений, либо пользователь не имеет доступа к чату
            raise UserNotInChat()
        
        return messages
    
    #Получение сообщения(медиа)
    async def get_media_message(self, user_id, message_id):
        #получаем тип сообщения по его id
        message_type = (await self.message_database.get_message_type(user_id, message_id)).get("message_type")
        if not message_type:#если none - пользователь не состоит в чате
            raise UserNotInChat()
        
        media_bytes = None
        #проверяем какой тип сообщения и получаем сам медиа файл
        match message_type:
            case MessageTypes.VOICE:
                media_bytes = await self.file_storage_service.get_voice_message(message_id)

            case _:
                raise UnknownMessageType()

        return media_bytes
    
    async def delete_message(self, message_id, user_id):
        chat_id = (await self.chat_database.get_chat_id_by_message(message_id)).get("chat_id")
        await self.messenger_realtime_service.delete_message(chat_id, message_id, user_id)
        await self.message_database.delete_message(message_id, user_id)

    async def edit_message(self, user_id, message_id, nonce, text):
        chat_id = (await self.chat_database.get_chat_id_by_message(message_id)).get("chat_id")
        await self.messenger_realtime_service.edit_message(chat_id, message_id, user_id, text, nonce)
        await self.message_database.edit_message(user_id, message_id, nonce, text)