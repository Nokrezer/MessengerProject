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
    async def send_message(self, text, message_type, nonce, sender_id, reader_id, chat_id, data):
        if reader_id:#Если передан id пользователя(получателя)(личный чат)
            chat_id = await self.chat_database.get_chat_by_members(sender_id, reader_id)
            
            if not chat_id:#Если чата не существует, создаём
                chat_id = await self._create_private_chat(sender_id=sender_id, reader_id=reader_id)
            else:
                chat_id = chat_id.get("chat_id")

        elif not chat_id:
            raise NeedChatOrUserId()
        
        message_id = uuid.uuid4().hex
        #Проверяем типы сообщений, если тип не текст, тогда сохраняем отправленный файл
        if message_type == MessageTypes.VOICE:
            await self.file_storage_service.save_voice_message(data, message_id)
        
        await self.message_database.send_message(sender_id=sender_id, chat_id=chat_id,
                                                text=text, nonce=nonce,
                                                message_id=message_id,
                                                message_type=message_type)#сохраняем сообщение в бд
        #отправляем соо в режиме реального времени(если пользователи онлайн)
        await self.messenger_realtime_service.send_message(chat_id, text, nonce, message_id, message_type, sender_id)

        return chat_id
    
    #Получение истории сообщений
    async def get_messages(self, user_id, chat_id, offset=0):
        #получаем, имеет ли пользователь доступ к чату
        access = await self.chat_database.check_user_access_to_chat(user_id, chat_id)
        
        if not access:
            raise UserNotInChat()
        
        return await self.message_database.get_messages(chat_id, offset)
    
    #Получение сообщения(медиа)
    async def get_media_message(self, user_id, message_id):
        #проверяем, есть ли у пользователя доступ к сообщению
        access = await self.chat_database.check_user_access_to_message(user_id, message_id)
        if not access:
            raise UserNotInChat()
        
        #получаем тип сообщения по его id
        message_type = (await self.message_database.get_message_type(message_id)).get("message_type")
        
        media_bytes = None
        #проверяем какой тип сообщения и получаем сам медиа файл
        match message_type:
            case MessageTypes.VOICE:
                media_bytes = await self.file_storage_service.get_voice_message(message_id)

            case _:
                raise UnknownMessageType()

        return media_bytes