from fastapi import Request, HTTPException, Response
from fastapi.responses import HTMLResponse, JSONResponse

from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from shared.responses import *
from shared.exceptions import *

from settings.config import *

from datetime import datetime, timedelta, timezone

class AuthController():
    def __init__(self, auth_service, token_service, log_database):
        self.auth_service = auth_service
        self.token_service = token_service
        self.log_database = log_database

    def _set_cookie_access(self, response, access_token):
        access_expires = (datetime.now() + timedelta(minutes=ACCESS_TOKEN_MINUTES)).astimezone(timezone.utc)
        response.set_cookie(key="ACCESS_TOKEN",
                            value=access_token,
                            httponly=True,
                            secure=USE_CERTS,#Если отключено использование сертификата, отключаем secure(Работает только с https)
                            samesite="lax",
                            expires=access_expires
                            )
    
    def _set_cookie_refresh(self, response, refresh_token):
        refresh_expires = (datetime.now() + timedelta(days=REFRESH_TOKEN_DAYS)).astimezone(timezone.utc)
        response.set_cookie(key="REFRESH_TOKEN",
                            value=refresh_token,
                            httponly=True,
                            secure=USE_CERTS, 
                            samesite="lax",
                            expires=refresh_expires
                            )

    #нужен для методов, которые возвращают токены.
    #Решает каким образом вернуть клиенту токены
    def _return_tokens(self, request:Request, access_token, refresh_token):
        client_agent = request.headers.get("user-agent")
            #Если запрос с браузер устанавливаем токены в куки
        if "Mozilla" in client_agent:
            response = SuccessResponse()
            
            #Устанавливаем куки для access и refresh токенов
            self._set_cookie_access(response=response, access_token=access_token)
            self._set_cookie_refresh(response=response, refresh_token=refresh_token)
                
            return response
        else:#Если какой-либо другой агент, возвращаем токены
            return {"ACCESS_TOKEN":access_token, "REFRESH_TOKEN":refresh_token}

    async def login(self, request:Request):
        try:
            form_data = await request.form()
            
            access_token, refresh_token = await self.auth_service.login(login=form_data.get("login"),
                                                                        password=form_data.get("password"))
            
            return self._return_tokens(request=request,
                                       access_token=access_token,
                                       refresh_token=refresh_token)
        
        except UserNotFound:
            raise HTTPException(detail="Пользователь не найден", status_code=404)
        
        except IncorrectPassword:
            raise HTTPException(detail="Неверный пароль", status_code=403)

        except Exception as error:
            await self.log_database.add_error(request.url.path, error)
            raise HTTPException(detail="Произошла ошибка", status_code=400)
        
    #Вход при помощи кода авторизации
    async def login_with_code(self, request:Request):
        try:
            form_data = await request.form()

            access_token, refresh_token = await self.auth_service.login_with_code(email=form_data.get("email"),
                                                                                  code=form_data.get("code"))
            
            return self._return_tokens(request=request,
                                       access_token=access_token,
                                       refresh_token=refresh_token)
        
        except NeedEmail:
            raise HTTPException(detail="Необходима почта", status_code=400)
        
        except NeedAuthCode:
            raise HTTPException(detail="Необходим код авторизации", status_code=400)

        except AuthCodeNotFinded:
            raise HTTPException(detail="Код авторизации не найден или срок действия истёк", status_code=404)
        
        except AuthCodeExpired:
            raise HTTPException(detail="Срок действия кода истёк", status_code=401)
        
        except Exception as error:
            await self.log_database.add_error(request.url.path, error)
            raise HTTPException(detail="Произошла ошибка", status_code=400)
        
    async def request_auth_code(self, request:Request):
        try:
            form_data = await request.form()

            await self.auth_service.request_auth_code(form_data.get("email"))

            return SuccessResponse()
        except UserNotFound:
            raise HTTPException(detail="Аккаунт с такой почтой не найден", status_code=400)
        
        except Exception as error:
            await self.log_database.add_error(request.url.path, error)
            raise HTTPException(detail="Произошла ошибка", status_code=400)
        
    async def request_reg_code(self, request:Request):
        try:
            form_data = await request.form()

            await self.auth_service.request_reg_code(form_data.get("email"))
            return SuccessResponse()
        
        except UserWithEmailExist:
            raise HTTPException(detail="Почта уже зарегистрирована", status_code=400)
        
        except Exception as error:
            await self.log_database.add_error(request.url.path, error)
            raise HTTPException(detail="Произошла ошибка", status_code=400)
    
    async def registration(self, request:Request):
        try:
            form_data = await request.form()#Получаем данные формы
            
            await self.auth_service.registration(form_data.get("code"), form_data.get("name"),
                                                 form_data.get("email"), form_data.get("password"))
            return SuccessResponse()
        
        except NeedEmail:
            raise HTTPException(detail="Требуется почта", status_code=400)
        
        except NeedPassword:
            raise HTTPException(detail="Требуется пароль", status_code=400)
        
        except AuthCodeNotFinded:
            raise HTTPException(detail="Требуется код регистрации", status_code=400)

        except UserWithEmailExist:
            raise HTTPException(detail="Пользователь с такой почтой существует", status_code=409)
        
        except Exception as error:
            await self.log_database.add_error(request.url.path, error)
            raise HTTPException(detail="Произошла ошибка", status_code=400)
        
    async def update_access_token(self, request: Request):
        try:
            if "Mozilla" in request.state.user_agent:
                response = SuccessResponse()
                
                access_token = await self.token_service.update_access_token(request.state.token)
                self._set_cookie_access(response=response, access_token=access_token)
                
                return response
            
            else:
                return {"ACCESS_TOKEN": await self.token_service.update_access_token(request.state.token)}
        
        except ExpiredSignatureError:
            raise HTTPException(detail="Срок действия токена истёк", status_code=401)
        
        except InvalidTokenError:
            raise HTTPException(detail="Неверная подпись токена", status_code=401)
        
        except TokenNotExists:
            raise HTTPException(detail="Токен не существует", status_code=401)

        except Exception as error:
            await self.log_database.add_error(request.url.path, error)
            raise HTTPException(detail="Произошла ошибка", status_code=400)
        
    async def verify_refresh_token(self, request: Request):
        try:
            await self.token_service.verify_refresh_token(request.state.token)
            return SuccessResponse()
            
        except ExpiredSignatureError:
            raise HTTPException(detail="Срок действия токена истёк", status_code=401)
        
        except InvalidTokenError:
            raise HTTPException(detail="Неверная подпись токена", status_code=401)
        
        except TokenNotExists:
            raise HTTPException(detail="Токен не существует", status_code=401)

        except Exception as error:
            await self.log_database.add_error(request.url.path, error)
            raise HTTPException(detail="Произошла ошибка", status_code=400)
    
    async def verify_access_token(self, request: Request):
        try:
            await self.token_service.verify_access_token(request.state.token)
            return SuccessResponse()
            
        except ExpiredSignatureError:
            raise HTTPException(detail="Срок действия токена истёк", status_code=401)
        
        except InvalidTokenError:
            raise HTTPException(detail="Неверная подпись токена", status_code=401)
        
        except TokenNotExists:
            raise HTTPException(detail="Токен не существует", status_code=401)

        except Exception as error:
            await self.log_database.add_error(request.url.path, error)
            raise HTTPException(detail="Произошла ошибка", status_code=400)
        
    async def get_temp_token(self, request:Request):
        try:
            return {"TEMP_TOKEN": await self.token_service.get_temp_token(request.state.token)}
        except Exception as error:
            await self.log_database.add_error(request.url.path, error)
            raise HTTPException(detail="Произошла ошибка", status_code=400)