from os import getenv

SERVER_IP = "0.0.0.0"
SERVER_PORT = 8000
#sql
SQL_HOST = "127.0.0.1"
SQL_PORT = 3306
SQL_USER = "root"
SQL_PASSWORD = "root"
SQL_DATABASE = "messenger"

API_PREFIX = "/api/"
AUTH_PREFIX = "/auth/"

#сроки действия
ACCESS_TOKEN_MINUTES = 10
REFRESH_TOKEN_DAYS = 10

HASH_ITERATIONS = 500_000

CERT = "../certificates/cert.pem"
CERT_KEY = "../certificates/cert_key.pem"
USE_CERTS = False#Если false сертификаты не используются

SALT_SIZE = 16

REFRESH_KEY = getenv("MESSENGER_REFRESH_KEY")
ACCESS_KEY = getenv("MESSENGER_ACCESS_KEY")
EMAILS_PEPPER = getenv("EMAILS_PEPPER").encode()
