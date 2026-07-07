import os

import base64
from cryptography.fernet import Fernet
import secrets
import hashlib

from settings.config import *

class CryptService():
    #метод для хэширования. Можно передавать множество данных, возвращает список данных и соль
    def hash(self, *args, salt=None):
        if not salt:
            salt = os.urandom(SALT_SIZE)

        hashes = []
        for data in args:
            hashes.append(
                hashlib.pbkdf2_hmac(
                    "sha256",
                    data.encode(),
                    salt,
                    HASH_ITERATIONS
                ))
            
        return *hashes, salt
    
    def hash_email(self, email):
        return hashlib.pbkdf2_hmac(
                    "sha256",
                    email.encode(),
                    EMAILS_PEPPER,
                    HASH_ITERATIONS
                )

    def __crypt_data(self, data, key):
        if type(data) == str:
            data = data.encode()

        digest = hashlib.sha256(key.encode('utf-8')).digest()
        key = base64.urlsafe_b64encode(digest)

        fernet = Fernet(key)
        
        return fernet.encrypt(data)
    
    def crypt_user_image(self, data, user_id):
        return self.__crypt_data(data, USER_IMAGE_PEPPER + user_id)
    
    def crypt_user_name(self, data, user_id):
        return self.__crypt_data(data, USER_NAME_PEPPER + user_id)
    
    def crypt_user_nickname(self, data, user_id):
        return self.__crypt_data(data, USER_NICKNAME_PEPPER + user_id)
    
    def crypt_user_bio(self, data, user_id):
        return self.__crypt_data(data, USER_BIO_PEPPER + user_id)
    
    def decrypt_user_image(self, data, user_id):
        return self.__decrypt_data(data, USER_IMAGE_PEPPER + user_id)
    
    def decrypt_user_name(self, data, user_id):
        return self.__decrypt_data(data, USER_NAME_PEPPER + user_id)
    
    def decrypt_user_nickname(self, data, user_id):
        return self.__decrypt_data(data, USER_NICKNAME_PEPPER + user_id)
    
    def decrypt_user_bio(self, data, user_id):
        return self.__decrypt_data(data, USER_BIO_PEPPER + user_id)
    
    def __decrypt_data(self, data, key):
        if type(data) == str:
            data = data.encode()

        digest = hashlib.sha256(key.encode('utf-8')).digest()
        key = base64.urlsafe_b64encode(digest)

        fernet = Fernet(key)

        return fernet.decrypt(data)
    
    def generate_auth_code(self):#генерация кода для авторизации
        secret_code = secrets.randbelow(10 ** AUTH_CODE_SIZE)

        return f"{secret_code:0{AUTH_CODE_SIZE}d}"