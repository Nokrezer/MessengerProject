from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

from contextlib import asynccontextmanager

from settings.config import *
from shared.responses import *
from shared.exceptions import *
from jwt.exceptions import DecodeError

#список запросов к медиа
media_requests = ["getUserImage", "getChatImage", "getMediaMessage"]

class BeforeRequestMiddleware():
    def __init__(self, token_service):
        self.token_service = token_service

    def register(self, server):
        @server.middleware("http")
        async def before_request(request: Request, func):
            #Получаем один из токенов от клиента
            
            request.state.token = (request.cookies.get("REFRESH_TOKEN")#для браузера(куки httpOnly + lax/strict)
                                   or request.cookies.get("ACCESS_TOKEN")#для браузера(куки httpOnly + lax/strict)
                                   or request.headers.get("Authorization")#для мобильного приложения
                                   or request.query_params.get("tempToken"))#для получения медиа(ТОКЕН ТОЛЬКО ДЛЯ МЕДИА)
            
            if request.url.path.startswith(API_PREFIX):
                try:
                    if not request.state.token:
                        raise NeedToken()
                    
                    #если запрос для получения медиа, проверяем временный токен
                    if request.url.path.replace(API_PREFIX, "") in media_requests:
                        token_data = self.token_service.decrypt_temp_token(request.state.token)
                    else:
                        token_data = await self.token_service.verify_access_token(request.state.token)
                    
                    request.state.user_id = token_data["user_id"]

                except NeedToken:
                    return HTMLResponse(content="Для доступа к сервису необходим токен", status_code=401)
                except DecodeError:
                    return HTMLResponse(content="Ошибка токена или неверный тип токена", status_code=401)
                except Exception as e:
                    return HTMLResponse(content=str(e), status_code=400)

            request.state.user_agent = request.headers.get("User-Agent")
            
            #Передаём запрос в вызываемую функцию
            response = await func(request)
            
            return response
        
class ServingMiddleware():
    def __init__(self, database):
        self.database = database

    @asynccontextmanager
    async def lifespan(self, server:FastAPI):
        await self.database.init()

        yield