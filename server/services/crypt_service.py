import hashlib
import os

from settings.config import *

class CryptService():
    # def __init__():
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

    