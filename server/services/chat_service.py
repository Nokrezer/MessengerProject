import uuid

from shared.exceptions import *
from shared.types import *

from settings.config import *

class ChatService():
    def __init__(self, chat_database, members_database, avatar_service, user_database, file_storage_service):
        self.chat_database = chat_database
        self.members_database = members_database
        self.avatar_service = avatar_service
        self.user_database = user_database
        self.file_storage_service = file_storage_service

    async def _exist_chat(self, chat_id):
        exist_chat = await self.chat_database.get_chat(chat_id=chat_id.replace('"', ""))

        if not exist_chat:#Если чат не найден в БД - ошибка
            raise ChatNotExist()
        
    async def _create_private_chat(self, sender_id, reader_id):
        chat_id = uuid.uuid4().hex
        
        await self.chat_database.create_private_chat(sender_id=sender_id,
                                            reader_id=reader_id,
                                            chat_id=chat_id)
        
        return chat_id
    
    async def _check_user_access_to_chat(self, user_id, chat_id):
        access = await self.chat_database.check_user_access_to_chat(user_id, chat_id)
        if not access:
            raise UserNotInChat()
    
    async def create_private_chat(self, sender_id, reader_id):
        #сначала пытаемся получить, есть ли у двух пользователей уже чат
        exist_chat = await self.chat_database.get_chat_by_members(sender_id, reader_id)
        if not exist_chat:#если не существует - создаём
            return await self._create_private_chat(sender_id, reader_id)
        
        return exist_chat["chat_id"]
    
    #Получение id чатов, в которых состоит пользователь
    async def get_user_chats(self, user_id):
        return await self.chat_database.get_user_chats(user_id)
    
    async def get_chat_data(self, chat_id, user_id):
        await self._check_user_access_to_chat(user_id, chat_id)
        
        return await self.chat_database.get_chat_data(chat_id)
    
    async def get_chat_type(self, chat_id):
        return await self.chat_database.get_chat_type(chat_id)
    
    async def get_chat_members(self, chat_id, user_id):
        await self._check_user_access_to_chat(user_id, chat_id)

        return await self.members_database.get_chat_members(chat_id)
    
    async def get_chat_by_members(self, sender_id, reader_id):
        return await self.chat_database.get_chat_by_members(sender_id, reader_id)
    
    async def get_chat_image(self, chat_id, user_id):
        #Получаем тип чата
        chat_type = (await self.chat_database.get_chat_type(chat_id))["chat_type"]
        
        if chat_type == ChatTypes.PRIVATE:
            #Получаем id собеседника
            second_user_id = (await self.chat_database.get_second_user_id(chat_id, user_id))["user_id"]
            
            #Получаем имя файла аватарки
            image_data = await self.user_database.get_user_image(second_user_id)

            #Если аватарка не получена, возвращаем общую аватарку
            if not image_data:
                return None#await self.file_storage_service._get_file_text(USERS_IMAGES + "user.svg")
            
            image_name = image_data.get("image_name")
            
            #получаем сами байты аватарки и возвращаем
            return await self.avatar_service.get_user_image(image_name, second_user_id)
        elif chat_type == ChatTypes.GROUP:
            pass

    async def create_group_chat(self, user_id):
        chat_id = uuid.uuid4().hex
        await self.chat_database.create_group_chat(user_id, chat_id)

        return chat_id
    
    async def add_members(self, raw_users_ids, chat_id):
        users_ids = []
        for user_id in raw_users_ids.split(" "):
            users_ids.append(chat_id)
            users_ids.append(user_id)

        await self.chat_database.add_members(users_ids)