from uuid import uuid4
import secrets
from datetime import datetime, timedelta, timezone

from settings.config import *
# from shared.exceptions import *

class AuthService():
    def __init__(self, auth_database, crypt_service, token_service, email_service, validation_service):
        self.auth_database = auth_database
        self.crypt_service = crypt_service
        self.token_service = token_service
        self.email_service = email_service
        self.validation_service = validation_service

    #получение аккаунта по нику или почте
    async def _get_account_by_login(self, login):
        account = None

        if self.validation_service.validate_email(login):#проверям, почта ли это
            email_hash = self.crypt_service.hash_email(login)
            account = await self.auth_database.login_by_email(email_hash)#Получаем аккаунт пользователя
        else:#Если передан ник и пароль
            account = await self.auth_database.login_by_nickname(login)

        return account

    async def login(self, login, password):
        self.validation_service.check_login_args(login, password)
        
        account = await self._get_account_by_login(login)
        self.validation_service.account_exist(account)#проверка, существует ли аккаунт
         
        password_hash, _ = self.crypt_service.hash(password, salt=account["salt"])
        #проверяем, сходятся ли хэши
        self.validation_service.check_hashes(password_hash, account.get("password_hash"))
        
        user_id = account.get("user_id")
        token_pair = await self.token_service.create_token_pair(user_id)
        
        return token_pair
        
    async def login_with_code(self, email, code):
        self.validation_service.check_code_login_args(email, code)

        email_hash = self.crypt_service.hash_email(email)
        
        account = await self.auth_database.login_by_email(email_hash)#Получаем аккаунт пользователя
        user_id = account.get("user_id")

        code_data = await self.auth_database.get_user_code(user_id=user_id, code=code)
        self.validation_service.exist_auth_code(code_data)

        #Делаем код недействительным(если есть в бд)
        await self.auth_database.revoke_code(user_id=user_id, code=code)
        self.validation_service.verify_auth_code(code_data.get("created_at"))
        
        return await self.token_service.create_token_pair(user_id)
    
    #отправка и сохранение в бд кода для регистрации
    async def request_reg_code(self, email):
        email_hash = self.crypt_service.hash_email(email)

        #Из БД получаем, привязана ли почта к какому-либо другому аккаунту
        user_data = await self.auth_database.login_by_email(email_hash)
        self.validation_service.exist_email(user_data)

        code = self.crypt_service.generate_auth_code()
        #сохраняем код с хэшом почты в БД
        await self.auth_database.add_reg_code(email_hash, code)
        #отправляем пользователю
        await self.email_service.send_reg_code(email, code)
    
    #отправка и сохранение в бд кода для входа
    async def request_auth_code(self, email):
        code = self.crypt_service.generate_auth_code()

        email_hash = self.crypt_service.hash_email(email)
        account = await self.auth_database.login_by_email(email_hash)#Получаем аккаунт пользователя
        self.validation_service.account_exist(account)#проверка, существует ли аккаунт
        
        #добавление кода в БД
        await self.auth_database.add_auth_code(account.get("user_id"), code)

        await self.email_service.send_auth_code(email, code)
        
    async def registration(self, code, name, email, password):
        self.validation_service.check_registration_args(name, email, password)
        
        email_hash = self.crypt_service.hash_email(email)

        code_data = await self.auth_database.get_user_code(email_hash=email_hash, code=code)
        self.validation_service.exist_auth_code(code_data)
        #делаем код недействительным
        await self.auth_database.revoke_code(code=code, email_hash=email_hash)
        
        user_id = uuid4().hex
        password_hash, salt = self.crypt_service.hash(password)
        await self.auth_database.registration(user_id=user_id, name=name, password_hash=password_hash,
                                              email_hash=email_hash, salt=salt)