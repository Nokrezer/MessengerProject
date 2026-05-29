from uuid import uuid4

from shared.exceptions import *

class AuthService():
    def __init__(self, auth_database, crypt_service, user_database, token_service, token_database):
        self.auth_database = auth_database
        self.user_database = user_database
        self.crypt_service = crypt_service
        self.token_service = token_service
        self.token_database = token_database

    # async def _token_type(self, token):#
    #     token_data = self.token_service.decrypt_token(token)
    #     return token_data["type"]
    
    async def login(self, login, password):
        if login == None or password == None:
            raise NotEnoughArguments()
        
        # email_hash = None
        account = None
        if "@" in login:#Если есть собачка, значит почта
            email_hash = self.crypt_service.hash_email(login)
            account = await self.auth_database.login_by_email(email_hash)#Получаем аккаунт пользователя
        else:
            account = await self.auth_database.login_by_nick_name(login)
        
        if not account:#Если аккаунт не найден в БД
            raise UserNotFound()
        
        password_hash, _ = self.crypt_service.hash(password, salt=account["salt"])
        
        if password_hash != account["password_hash"]:#Если хэши не сходятся
            raise IncorrectPassword()
        
        access_token = self.token_service.create_access_token(account["user_id"])
        refresh_token, token_id = self.token_service.create_refresh_token(account["user_id"])

        await self.token_database.add_refresh_token(token_id, account["user_id"])
        
        return access_token, refresh_token

    async def registration(self, name, email, password):
        if name == None or email == None or password == None:
            raise NotEnoughArguments()
        
        email_hash = self.crypt_service.hash_email(email)
        #Из БД получаем, привязана ли почта к какому-либо другому аккаунту
        email_exist = await self.user_database.get_user_by_email_hash(email_hash)
        if email_exist:
            raise UserWithEmailExist()
        
        user_id = uuid4().hex
        
        password_hash, salt = self.crypt_service.hash(password)
        
        await self.auth_database.registration(user_id=user_id, name=name, password_hash=password_hash,
                                              email_hash=email_hash, salt=salt)

    async def update_access_token(self, token):
        #Получаем данные токена, если срок действия токена вышел - ошибка
        token_data = self.token_service.decrypt_refresh_token(token)

        # if token_data["type"] != "refresh":
        #     raise NeedRefreshToken()
        
        #Получае токен из БД, чтобы проверить существование
        token_exist = await self.token_database.get_refresh_token(token_data["jti"])
        
        if not token_exist:
            raise TokenNotExistsInDatabase

        return self.token_service.create_access_token(token_data["user_id"])

