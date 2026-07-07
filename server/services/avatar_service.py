import uuid

class AvatarService():
    def __init__(self, image_service, file_storage_service, crypt_service):
        self.image_service = image_service
        self.file_storage_service = file_storage_service
        self.crypt_service = crypt_service

    #обновляет аватарку пользователя и удаляет прошлую. Возвращает название нового файла
    async def update_user_image(self, past_name, new_image, user_id):
        if past_name:
            try:
                self.file_storage_service.delete_user_image(past_name)
            except: pass

        #обработка данного изображения
        pillow_image = self.image_service.image_from_bytes(new_image)
        cropped_image = self.image_service.cut_image(pillow_image)
        compressed_image = self.image_service.compress_image(cropped_image)
        #шифруем изображение пользователя
        crypted_image = self.crypt_service.crypt_user_image(compressed_image, user_id)
        
        new_image_name = uuid.uuid4().hex
        #сохраняем изображение пользователя
        await self.file_storage_service.new_user_image(crypted_image, new_image_name)

        return new_image_name
    
    async def get_user_image(self, image_name, user_id):
        crypted_image = await self.file_storage_service.get_user_image(image_name)
        decrypted_image = self.crypt_service.decrypt_user_image(crypted_image, user_id)
        
        return decrypted_image