from os import getenv

SERVER_IP = "0.0.0.0"
SERVER_PORT = 8000
REALTIME_PORT = 8010
#sql
SQL_HOST = "127.0.0.1"
SQL_PORT = 3306
SQL_USER = "root"
SQL_PASSWORD = "root"
SQL_DATABASE = "messenger"

API_PREFIX = "/api/"
AUTH_PREFIX = "/auth/"

#сроки действия
TEMP_TOKEN_MINUTES = 1
ACCESS_TOKEN_MINUTES = 10
REFRESH_TOKEN_DAYS = 10
AUTH_CODE_MINUTES = 5

HASH_ITERATIONS = 500_000

CERT = "../certificates/cert.pem"
CERT_KEY = "../certificates/cert_key.pem"
USE_CERTS = False#Если false сертификаты не используются

SALT_SIZE = 16

#ключи
REFRESH_KEY = getenv("MESSENGER_REFRESH_KEY")
ACCESS_KEY = getenv("MESSENGER_ACCESS_KEY")
TEMP_KEY = getenv("MESSENGER_TEMP_KEY")
EMAILS_PEPPER = getenv("EMAILS_PEPPER").encode()
USER_IMAGE_PEPPER = getenv("USER_IMAGE_PEPPER")
USER_NAME_PEPPER = getenv("USER_NAME_PEPPER")
USER_NICKNAME_PEPPER = getenv("USER_NICKNAME_PEPPER")
USER_BIO_PEPPER = getenv("USER_BIO_PEPPER")
CHAT_IMAGE_PEPPER = getenv("CHAT_IMAGE_PEPPER")

#расположение пользовательских данных(аватарки)
USERS_DATA = "/home/nokrezer/Рабочий стол/MessengerProject/usersData/"
USERS_IMAGES = USERS_DATA + "usersImages/"
#расположение данных чатов(голосовые сообщения, картинки и тд)
CHATS_DATA = "/home/nokrezer/Рабочий стол/MessengerProject/chatsData/"
VOICE_MESSAGES = CHATS_DATA + "voiceMessages/"

#Обрезка изображений
SIDES_CUT = 150#Обрезка по сторонам
HEIGHT_CUT = 50#Обезка сверху и снизу
IMAGE_QUALITY = 20#Меньше число = меньше размер
CUT_SPEED = 4#Скорость сжатия
IMAGE_STANDART = 1024#Размер изображения на который можно опираться

#ОГРАНИЧЕНИЯ
MAX_MESSAGES = 100#Сколько сообщений клиент может получить за раз
NAME_MIN_LEN = 1#минимальный размер имени который должен быть
NICKNAME_MIN_LEN = 3#минимальный размер ника который должен быть
BIO_MAX_LEN = 1000#максимальный размер описания профиля
AUTH_CODE_SIZE = 6#размер кода для авторизации

#Настройки отправки сообщений по почте
EMAIL_SMTP = "smtp.gmail.com"
EMAIL_SENDER = getenv("EMAIL_SENDER")
EMAIL_APP_PASSWORD = getenv("EMAIL_APP_PASSWORD")
EMAIL_SMTP_PORT = 587