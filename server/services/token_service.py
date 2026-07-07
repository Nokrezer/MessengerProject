import jwt
from datetime import datetime, timedelta, timezone
import uuid

from settings.config import *
from shared.exceptions import *

class TokenService():
    def __init__(self, token_database):
        self.token_database = token_database

    #Метод для проверки в БД существования токена и не отозван ли он
    async def exist_refresh_token(self, jti):
        exist_token = await self.token_database.get_refresh_token(jti)
        if not exist_token:
            raise TokenNotExists()
        
    def create_access_token(self, user_id, refresh_jti):
        token_data = {"type":"access",
                      "user_id":user_id,
                      "refresh_jti":refresh_jti,
                      "exp":datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_MINUTES)}
        
        token = jwt.encode(token_data, ACCESS_KEY, "HS256")
        return token
    
    async def create_refresh_token(self, user_id):
        jti = uuid.uuid4().hex#jti = token id

        token_data = {"type":"refresh",
                      "user_id":user_id,
                      "exp":datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_DAYS),
                      "jti":jti}
        
        token = jwt.encode(token_data, REFRESH_KEY, "HS256")

        await self.token_database.add_refresh_token(jti, user_id)

        return token, jti
    
    #токен для получения медиа
    def create_temp_token(self, user_id):
        token_data = {"type":"temp",
                      "user_id":user_id,
                      "exp":datetime.now(timezone.utc) + timedelta(minutes=TEMP_TOKEN_MINUTES)}
        
        token = jwt.encode(token_data, TEMP_KEY, "HS256")
        return token
    
    #генерирует и возвращает refresh, access токены
    async def create_token_pair(self, user_id):
        refresh_token, token_id = await self.create_refresh_token(user_id)
        access_token = self.create_access_token(user_id, token_id)

        return access_token, refresh_token
    
    def _decrypt_refresh_token(self, token):
        if type(token) == str:
            token = token.encode()
            
        token_data = jwt.decode(token, REFRESH_KEY, algorithms=["HS256"])
        
        return token_data

    def _decrypt_access_token(self, token):
        if type(token) == str:
            token = token.encode()
            
        token_data = jwt.decode(token, ACCESS_KEY, algorithms=["HS256"])
        return token_data
    
    def decrypt_temp_token(self, token):
        if type(token) == str:
            token = token.encode()

        token_data = jwt.decode(token, TEMP_KEY, algorithms=["HS256"])
        return token_data
        
    async def update_access_token(self, token):
        #Получаем данные токена, если срок действия токена вышел - ошибка
        token_data = await self.verify_refresh_token(token)
        return self.create_access_token(token_data["user_id"], token_data["jti"])
        
    async def verify_refresh_token(self, token):
        token_data = self._decrypt_refresh_token(token)
        await self.exist_refresh_token(token_data["jti"])
        
        return token_data
    
    async def verify_access_token(self, token):
        token_data = self._decrypt_access_token(token)
        await self.exist_refresh_token(token_data["refresh_jti"])

        return token_data
    
    async def get_temp_token(self, refresh_token):
        token_data = await self.verify_refresh_token(refresh_token)
        return self.create_temp_token(token_data.get("user_id"))