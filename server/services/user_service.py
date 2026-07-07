from settings.config import *
from shared.exceptions import *

class UserService():
    def __init__(self, token_service, user_database, avatar_service, crypt_service, file_storage_service):
        self.token_service = token_service
        self.user_database = user_database
        self.avatar_service = avatar_service
        self.crypt_service = crypt_service
        self.file_storage_service = file_storage_service

    #Получение данных пользователя по его id
    async def get_user_data(self, user_id):
        return await self.user_database.get_user_by_id(user_id)
    
    #в бд ищем пользователей с сходим ником
    async def get_users(self, nickname):
        if len(nickname) == 0:
            return []
        
        return await self.user_database.get_users(nickname)
    
    async def get_user_by_chat_id(self, sender_id, chat_id):
        return await self.user_database.get_user_by_chat_id(sender_id, chat_id)
    
    async def set_user_image(self, user_id, image):
        #для начала получаем название изображения
        image_name = (await self.user_database.get_user_image(user_id))["image_name"]

        new_image_name = await self.avatar_service.update_user_image(image_name, image, user_id)

        #сохраняем название нового изображения в БД
        await self.user_database.set_user_image(user_id, new_image_name)

    async def get_user_image(self, user_id):
        image_data = await self.user_database.get_user_image(user_id)
        
        image_name = image_data.get("image_name")
        if not image_name:
            return None
            # return await self.file_storage_service._get_file_text(USERS_IMAGES + "user.svg")
        
        return await self.avatar_service.get_user_image(image_name, user_id)
    
    async def set_user_name(self, user_id, new_name):
        if not new_name:
            raise EmptyName()
        
        formated_name = new_name.replace(" ", "")
        #если имя короче указанного размера в конфиге
        if len(formated_name) < NAME_MIN_LEN:
            raise TooShortName()
        
        # crypted_name = self.crypt_service.crypt_user_name(new_name, user_id)
        await self.user_database.set_user_name(user_id, new_name)

    async def set_user_nickname(self, user_id, new_nickname):
        if not new_nickname:
            raise EmptyNickname()
        
        formated_nickname = new_nickname.replace(" ", "")
        #если имя короче указанного размера в конфиге
        if len(formated_nickname) < NICKNAME_MIN_LEN:
            raise TooShortNickName()
        
        await self.user_database.set_user_nickname(user_id, new_nickname)

    async def set_user_bio(self, user_id, bio):
        if not bio:#Если описание пустое(НЕ ПЕРЕДАНО В ЗАПРОСЕ), то ничего не делаем
            return
        
        if len(bio) > BIO_MAX_LEN:
            raise TooLongBio()
        
        await self.user_database.set_user_bio(user_id, bio)