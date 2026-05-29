from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

from contextlib import asynccontextmanager

from settings.config import *
from shared.responses import *
from shared.exceptions import *
from jwt.exceptions import DecodeError

class BeforeRequestMiddleware():
    def __init__(self, server, token_service, auth_controller):
        self.server = server
        self.token_service = token_service
        self.auth_controller = auth_controller

        @self.server.middleware("http")
        async def before_request(request: Request, func):
            #Получаем один из токенов от клиента
            request.state.token = request.cookies.get("REFRESH_TOKEN") or request.cookies.get("ACCESS_TOKEN") or request.headers.get("Authorization")
            
            if request.url.path.startswith(API_PREFIX):
                # response = await self.auth_controller._auth_token(request)

                # if response:
                #     return response
                try:
                    if not request.state.token:
                        raise NeedToken()
                    
                    token_data = self.token_service.decrypt_access_token(request.state.token)
                    token_type = token_data["type"]

                    #Если к авторизации с токеном access, ошибка
                    # if request.url.path.startswith(AUTH_PREFIX) and token_type == "access":
                    #     raise NeedRefreshToken()
                    #Если к api с токеном refresh, ошибка
                    # elif request.url.path.startswith(API_PREFIX) and token_type == "refresh":
                    #     raise NeedAccessToken()
                    
                    request.state.user_id = token_data["user_id"]
                except NeedRefreshToken:
                    return HTMLResponse(content="Неверный токен, нужен токен типа refresh", status_code=401)
                
                except NeedToken:
                    return HTMLResponse(content="Для доступа к сервису необходим токен", status_code=401)
                
                except NeedAccessToken:
                    return HTMLResponse(content="Неверный токен, нужен токен типа access", status_code=401)
                
                except DecodeError:
                    return HTMLResponse(content="Ошибка токена", status_code=401)
                
                except Exception as e:
                    return HTMLResponse(content=str(e), status_code=400)

            request.state.user_agent = request.headers.get("User-Agent")
            
            #Передаём запрос в вызываемую функцию
            response = await func(request)
            
            # response.headers["Access-Control-Allow-Origin"] = "*"
            # response.headers["Access-Control-Allow-Headers"] = "*"
            # response.headers["Access-Control-Allow-Methods"] = "*"
            
            return response
        
class ServingMiddleware():
    def __init__(self, database):
        self.database = database

    @asynccontextmanager
    async def lifespan(self, server:FastAPI):
        await self.database.init()

        yield