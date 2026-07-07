import aiofiles
import uuid
import os

from settings.config import *

class FileStorageService:
    async def _get_file(self, dir):
        async with aiofiles.open(dir, "rb") as file:
            return await file.read()
        
    async def _save_file_bytes(self, dir, data):
        async with aiofiles.open(dir, "wb") as file:
            await file.write(data)

    async def _get_file_text(self, dir):
        async with aiofiles.open(dir, "r") as file:
            return await file.read()

    async def _save_file_text(self, dir, data):
        async with aiofiles.open(dir, "w") as file:
            await file.write(data)
        
    def delete_user_image(self, name):
        os.remove(USERS_IMAGES + name + ".jpg")

    async def new_user_image(self, image_bytes, image_name):
        await self._save_file_bytes(USERS_IMAGES + image_name + ".jpg", image_bytes)
        
    async def get_user_image(self, name):
        return await self._get_file(USERS_IMAGES + name + ".jpg")
    
    # async def get_chat_image(self, name):
    #     return await self._get_file(CHATS_IMAGES + name + ".jpg")

    async def save_voice_message(self, voice_bytes, voice_name):
        await self._save_file_text(VOICE_MESSAGES + voice_name, voice_bytes)

    async def get_voice_message(self, voice_name):
        return await self._get_file_text(VOICE_MESSAGES + voice_name)