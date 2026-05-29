
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

#Сервисы
from services.auth_service import AuthService
from services.crypt_service import CryptService
from services.token_service import TokenService
from services.messenger_service import MessengerService
from services.user_service import UserService

#Управление маршрутами
from settings.routes import RegisterRoutes

#middleware
from middleware.requests import *

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import asyncio

class Core():
    def __init__(self):
        #БД
        self.database = Database()
        self.auth_database = AuthDatabase(self.database)
        self.user_database = UserDatabase(self.database)
        self.token_database = TokenDatabase(self.database)
        self.message_database = MessageDatabase(self.database)
        self.chat_database = ChatDatabase(self.database)

        self.serving_middleware = ServingMiddleware(self.database)
        #Сервер
        self.server = FastAPI(lifespan=self.serving_middleware.lifespan)

        #Сервисы
        self.crypt_service = CryptService()
        self.token_service = TokenService()
        self.messenger_service = MessengerService(message_database=self.message_database,
                                                  chat_database=self.chat_database)
        self.auth_service = AuthService(auth_database=self.auth_database,
                                        crypt_service=self.crypt_service,
                                        user_database=self.user_database,
                                        token_service=self.token_service,
                                        token_database=self.token_database)
        self.user_service = UserService(token_service=self.token_service,
                                        user_database=self.user_database)
        

        #Контроллеры
        self.api_controller = ApiController(messenger_service=self.messenger_service,
                                            user_service=self.user_service,
                                            token_service=self.token_service)
        self.auth_controller = AuthController(auth_service=self.auth_service,
                                              token_service=self.token_service)

        #Маршруты
        self.register_routers = RegisterRoutes(self.api_controller, self.auth_controller,
                                               self.server)
        
        #Middleware
        self.before_request = BeforeRequestMiddleware(self.server, self.token_service,
                                                      self.auth_controller)
        self.server.add_middleware(
            CORSMiddleware,
            allow_origins=[
                        "http://127.0.0.1:8081",
                        "http://192.168.31.168:8000",
                        "http://192.168.31.168:8081",
                        "http://localhost:8081"
                    ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            # expose_headers=["Set-Cookie"],
        )
        #Регистрируем маршруты сервера
        self.register_routers.register()