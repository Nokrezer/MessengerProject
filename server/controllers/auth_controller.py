from fastapi import Request, HTTPException, Response
from fastapi.responses import HTMLResponse, JSONResponse

from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from shared.responses import *
from shared.exceptions import *

from settings.config import *

from datetime import datetime, timedelta, timezone

class AuthController():
    def __init__(self, auth_service, token_service):
        self.auth_service = auth_service
        self.token_service = token_service

    # async def _auth_token(self, request:Request):
        # try:
        #     #Получаем один из двух токенов
        #     token = request.state.access_token or request.state.request_token
            
        #     token_data = self.token_service.decrypt_token(token)
        #     token_type = token_data["type"]

        #     #Если к авторизации с токеном access, ошибка
        #     if request.url.path.startswith(AUTH_PREFIX) and token_type == "access":
        #         raise NeedRefreshToken()
        #     #Если к api с токеном refresh, ошибка
        #     elif request.url.path.startswith(API_PREFIX) and token_type == "refresh":
        #         raise NeedAccessToken()
            
        #     request.state.user_id = token_data["user_id"]
        # except NeedRefreshToken:
        #     return HTMLResponse(content="Неверный токен, нужен токен типа refresh", status_code=401)
        
        # except NeedAccessToken:
        #     return HTMLResponse(content="Неверный токен, нужен токен типа access", status_code=401)
            
        # except Exception as e:
        #     return HTMLResponse(content=str(e), status_code=400)

    async def login(self, request:Request):
        try:
            form_data = await request.form()
            
            access_token, refresh_token = await self.auth_service.login(login=form_data.get("login"),
                                                                        password=form_data.get("password"))
            
            client_agent = request.headers.get("user-agent")
            #Если запрос с браузер устанавливаем токены в куки
            if "Mozilla" in client_agent:
                response = SuccessResponse()
                
                access_expires = (datetime.now() + timedelta(minutes=ACCESS_TOKEN_MINUTES)).astimezone(timezone.utc)
                response.set_cookie(key="ACCESS_TOKEN",
                                    value=access_token,
                                    httponly=True,
                                    secure=USE_CERTS,#Если отключено использование сертификата, отключаем secure(Работает только с https)
                                    samesite="lax",
                                    expires=access_expires
                                    )
                
                refresh_expires = (datetime.now() + timedelta(days=REFRESH_TOKEN_DAYS)).astimezone(timezone.utc)
                response.set_cookie(key="REFRESH_TOKEN",
                                    value=refresh_token,
                                    httponly=True,
                                    secure=USE_CERTS, 
                                    samesite="lax",
                                    expires=refresh_expires
                                    )
                
                return response
            else:#Если какой-либо другой агент, возвращаем токены
                return {"ACCESS_TOKEN":access_token, "REFRESH_TOKEN":refresh_token}
        
        except UserNotFound:
            raise HTTPException(detail="Пользователь не найден", status_code=404)
        
        except IncorrectPassword:
            raise HTTPException(detail="Неверный пароль", status_code=403)

        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)
    
    async def registration(self, request:Request):
        try:
            form_data = await request.form()#Получаем данные формы
            
            await self.auth_service.registration(form_data.get("name"), form_data.get("email"),
                                                 form_data.get("password"))
            return SuccessResponse()
        
        except NotEnoughArguments:
            raise HTTPException(detail="Все поля должны быть заполнены", status_code=400)
        
        except UserWithEmailExist:
            raise HTTPException(detail="Пользователь с такой почтой существует", status_code=409)
        
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)
        
    async def update_access_token(self, request: Request):
        try:
            if "Mozilla" in request.state.user_agent:
                response = SuccessResponse()
                
                access_token = await self.auth_service.update_access_token(request.state.token)
                samesite = "None"#"lax" if USE_CERTS else None
                
                access_expires = (datetime.now() + timedelta(minutes=ACCESS_TOKEN_MINUTES)).astimezone(timezone.utc)
                response.set_cookie(key="ACCESS_TOKEN",
                                    value=access_token,
                                    httponly=True, 
                                    secure=USE_CERTS,#Если отключено использование сертификата, отключаем secure(Работает только с https)
                                    samesite=samesite,
                                    expires=access_expires,
                                    )
                
                return response
            
            else:
                return {"ACCESS_TOKEN": await self.auth_service.update_access_token(request.state.token)}
        
        except ExpiredSignatureError:
            raise HTTPException(detail="Срок действия токена истёк", status_code=401)
        
        except InvalidTokenError:
            raise HTTPException(detail="Неверная подпись токена", status_code=401)
        
        except TokenNotExistsInDatabase:
            raise HTTPException(detail="Неверный токен", status_code=401)

        except Exception as e:
            print(e)
            raise HTTPException(detail=str(e), status_code=400)
        
    async def verify_refresh_token(self, request: Request):
        try:
            self.token_service.decrypt_refresh_token(request.state.token)
            return SuccessResponse()
            
        except ExpiredSignatureError:
            raise HTTPException(detail="Срок действия токена истёк", status_code=401)
        
        except InvalidTokenError:
            raise HTTPException(detail="Неверная подпись токена", status_code=401)
        
        except TokenNotExistsInDatabase:
            raise HTTPException(detail="Неверный токен", status_code=401)

        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)
    
    async def verify_access_token(self, request: Request):
        try:
            self.token_service.decrypt_access_token(request.state.token)
            return SuccessResponse()
            
        except ExpiredSignatureError:
            raise HTTPException(detail="Срок действия токена истёк", status_code=401)
        
        except InvalidTokenError:
            raise HTTPException(detail="Неверная подпись токена", status_code=401)
        
        except TokenNotExistsInDatabase:
            raise HTTPException(detail="Неверный токен", status_code=401)

        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)