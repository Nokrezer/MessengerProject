from datetime import datetime, timezone, timedelta

from shared.exceptions import *
from settings.config import *

class ValidationService():
    def _validate_email(self, email):
        if not email: raise NeedEmail()
    
    def _validate_password(self, password):
        if not password: raise NeedPassword()

    #проверка аргументов при входе
    def check_login_args(self, login, password):
        if not login: raise NeedLogin()
        
        self._validate_password(password)

    def check_code_login_args(self, email, code):
        if not email: raise NeedEmail()
        if not code: raise NeedAuthCode()

    def exist_auth_code(self, code_data):
        if not code_data: raise AuthCodeNotFinded()
    
    #проверка аргументов при регистрации
    def check_registration_args(self, name, email, password):
        formated_name = name.replace(" ", "") if name else None
        if not formated_name or len(formated_name) == 0: raise NeedName()
        
        self._validate_email(email)
        
        self._validate_password(password)
    
    #проверка, существует ли почта
    def exist_email(self, data):
        if data: raise UserWithEmailExist()

    def check_hashes(self, hash_1, hash_2):
        if hash_1 != hash_2: raise IncorrectPassword()
        
    #проверка, существует ли аккаунт
    def account_exist(self, account):
        #Если аккаунт не найден в БД
        if not account: raise UserNotFound()

    def verify_auth_code(self, created_at):
        expired_at = created_at.astimezone(timezone.utc) + timedelta(minutes=AUTH_CODE_MINUTES)
        #проверяем срок годности кода
        if datetime.now(timezone.utc) > expired_at:
            raise AuthCodeExpired()
        
    def validate_email(self, email):
        #проверяем почту по точке и собачке
        if "@" in email and "." in email:
            return True
        else:
            return False