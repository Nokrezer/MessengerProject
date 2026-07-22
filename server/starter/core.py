#Управление маршрутами
from settings.routes import Routes



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from zstd_asgi import ZstdMiddleware

import asyncio

class Core():
    def __init__(self, api_controller, auth_controller, before_request_middleware, serving_middleware, realtime_core):
        self.api_controller = api_controller
        self.auth_controller = auth_controller
        self.realtime_core = realtime_core
        self.serving_middleware = serving_middleware
        self.before_request_middleware = before_request_middleware

        #Сервер
        self.server = FastAPI(lifespan=self.serving_middleware.lifespan)
        self.server.add_middleware(ZstdMiddleware, minimum_size=200, level=19)
        #Маршруты
        self.routes = Routes(self.api_controller, self.auth_controller, self.server, self.realtime_core)
        
        # self.server.add_middleware(
        #     CORSMiddleware,
        #     allow_origins=[
        #                 "http://127.0.0.1:8081",
        #                 "http://localhost:8081"
        #             ],
        #     allow_credentials=True,
        #     allow_methods=["*"],
        #     allow_headers=["*"]
        # )
        #регистрация middleware, для срабатывания перед каждым запросом
        self.before_request_middleware.register(server=self.server)
        #Регистрируем маршруты сервера
        self.routes.register()