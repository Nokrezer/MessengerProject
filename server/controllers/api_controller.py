from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from shared.responses import SuccessResponse

from shared.exceptions import *

class ApiController():
    def __init__(self, messenger_service, user_service, token_service):
        self.messenger_service = messenger_service
        self.user_service = user_service
        self.token_service = token_service

    #Полчение данных аккаунта по токену из БД
    async def get_id_by_token(self, request: Request):
        # print(1)
        # user_id = self.token_service.decrypt(request.state.token)["user_id"]
        # print(user_id)
        return JSONResponse(content={"user_id":request.state.user_id}, status_code=200)
        
    async def send_message(self, request: Request):
        try:
            form_data = await request.form()
            
            await self.messenger_service.send_message(
                                                    sender_id=request.state.user_id,
                                                    reader_id=form_data.get('reader_id'),
                                                    chat_id=form_data.get('chat_id'),
                                                    message_type=form_data.get("message_type"),
                                                    nonce=form_data.get("nonce"),
                                                    message=form_data.get("message")
                                                    )
            
            return SuccessResponse()
        
        except NeedChatOrUserId:
            HTTPException(detail="Нужен id чата или пользователя", status_code=400)

        except ChatNotExist:
            HTTPException(detail="Чат не найден", status_code=400)
            
        except Exception as e:
            HTTPException(detail=str(e), status_code=400)

    async def get_user_chats(self, request:Request):
        try:
            return await self.messenger_service.get_user_chats(request.state.user_id)
        
        except Exception as e:
            HTTPException(detail=str(e), status_code=400)
