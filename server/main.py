import uvicorn


#Конфигурация
from settings.config import *
#ядра сервера
from starter.core import Core
from starter.realtime_core import RealTimeCore, RealTimeState

#Контроллеры
from controllers.api_controller import ApiController
from controllers.auth_controller import AuthController

#БД
from database.database import Database
from database.user_database import UserDatabase
from database.auth_database import AuthDatabase
from database.token_database import TokenDatabase
from database.chat_database import ChatDatabase
from database.message_database import MessageDatabase
from database.key_database import KeyDatabase
from database.members_database import MembersDatabase

#Сервисы
from services.auth_service import AuthService
from services.crypt_service import CryptService
from services.token_service import TokenService
from services.messenger_service import MessengerService
from services.user_service import UserService
from services.key_service import KeyService
from services.image_service import ImageService
from services.file_storage_service import FileStorageService
from services.avatar_service import AvatarService
from services.chat_service import ChatService
from services.validation_service import ValidationService
from services.email_service import EmailService

#Сервисы для режима реального времени
from services.realtime_services.messenger_realtime_service import MessengerRealtimeService

#middleware
from middleware.requests import *

class ServiceContainer():
    def __init__(self):
        #БД
        self.database = Database()
        self.auth_database = AuthDatabase(self.database)
        self.user_database = UserDatabase(self.database)
        self.token_database = TokenDatabase(self.database)
        self.message_database = MessageDatabase(self.database)
        self.chat_database = ChatDatabase(self.database)
        self.key_database = KeyDatabase(self.database)
        self.members_database = MembersDatabase(self.database)

        #все состояния для ядра реального времени
        self.realtime_state = RealTimeState()

        #сервисы в режиме реал тайм
        self.messenger_realtime_service = MessengerRealtimeService(self.realtime_state)

        #Сервисы
        self.email_service = EmailService()
        self.validation_service = ValidationService()
        self.file_storage_service = FileStorageService()
        self.image_service = ImageService()
        self.crypt_service = CryptService()
        self.token_service = TokenService(token_database=self.token_database)
        self.avatar_service = AvatarService(image_service=self.image_service,
                                            file_storage_service=self.file_storage_service,
                                            crypt_service=self.crypt_service)
        self.chat_service = ChatService(chat_database=self.chat_database,
                                        members_database=self.members_database,
                                        avatar_service=self.avatar_service,
                                        user_database=self.user_database,
                                        file_storage_service=self.file_storage_service)
        self.messenger_service = MessengerService(message_database=self.message_database,
                                                  messenger_realtime_service=self.messenger_realtime_service,
                                                  file_storage_service=self.file_storage_service,
                                                  chat_database=self.chat_database)
        self.auth_service = AuthService(auth_database=self.auth_database,
                                        crypt_service=self.crypt_service,
                                        token_service=self.token_service,
                                        validation_service=self.validation_service,
                                        email_service=self.email_service)
        
        self.user_service = UserService(token_service=self.token_service,
                                        user_database=self.user_database,
                                        avatar_service=self.avatar_service,
                                        crypt_service=self.crypt_service,
                                        file_storage_service=self.file_storage_service)
        self.key_service = KeyService(key_database=self.key_database, user_service=self.user_service)
        
        #Контроллеры
        self.api_controller = ApiController(messenger_service=self.messenger_service,
                                            user_service=self.user_service,
                                            token_service=self.token_service,
                                            key_service=self.key_service,
                                            chat_service=self.chat_service)
        self.auth_controller = AuthController(auth_service=self.auth_service,
                                              token_service=self.token_service)
        
        #middleware
        self.serving_middleware = ServingMiddleware(self.database)
        self.before_request_middleware = BeforeRequestMiddleware(self.token_service)
        
        #ядро для режима реального времени
        self.realtime_core = RealTimeCore(self.token_service, self.realtime_state, self.chat_database)

class RunServer():
    def __init__(self, core):
        self.core = core

    def run_uvicorn(self):#обычный сервер(асинхронная обертка)
        uvicorn.run(self.core.server, host=SERVER_IP, port=SERVER_PORT,
                        ssl_keyfile=CERT_KEY if USE_CERTS else None,
                        ssl_certfile=CERT if USE_CERTS else None)

def main():
    container = ServiceContainer()

    core = Core(api_controller=container.api_controller, auth_controller=container.auth_controller,
                before_request_middleware=container.before_request_middleware,
                serving_middleware=container.serving_middleware,
                realtime_core=container.realtime_core)#Обычное ядро
    
    run_server = RunServer(core)
    run_server.run_uvicorn()

if __name__ == "__main__":
    main()