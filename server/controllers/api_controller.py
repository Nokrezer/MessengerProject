from fastapi import Request, HTTPException, Response
from fastapi.responses import JSONResponse

from shared.responses import SuccessResponse

from shared.exceptions import *
from settings.config import *

class ApiController():
    def __init__(self, messenger_service, user_service, token_service, key_service, chat_service):
        self.messenger_service = messenger_service
        self.user_service = user_service
        self.token_service = token_service
        self.key_service = key_service
        self.chat_service = chat_service

    #Полчение данных аккаунта по токену из БД
    async def get_id_by_token(self, request: Request):
        return JSONResponse(content={"user_id":request.state.user_id}, status_code=200)
        
    async def send_message(self, request: Request):
        try:
            form_data = await request.form()
            
            chat_id = await self.messenger_service.send_message(
                                                    sender_id=request.state.user_id,
                                                    reader_id=form_data.get('reader_id'),
                                                    chat_id=form_data.get('chat_id'),
                                                    message_type=form_data.get("message_type"),
                                                    nonce=form_data.get("nonce"),
                                                    text=form_data.get("text"),
                                                    data=form_data.get("data")
                                                    )
            
            return {"chat_id":chat_id}
        
        except NeedChatOrUserId:
            raise HTTPException(detail="Нужен id чата или пользователя", status_code=400)

        except ChatNotExist:
            raise HTTPException(detail="Чат не найден", status_code=400)
            
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)

    async def get_media_message(self, messageId:str, messageType:str, request:Request):
        try:
            return await self.messenger_service.get_media_message(messageId, messageType, request.state.user_id)
        except UserNotInChat:
            raise HTTPException(detail='Доступ запрещен', status_code=403)
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)

    async def get_user_chats(self, request:Request):
        try:
            return await self.chat_service.get_user_chats(request.state.user_id)
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)

    async def save_public_keys(self, request:Request):
        try:
            form_data = await request.form()

            await self.key_service.save_public_keys(request.state.user_id,
                                                   form_data.get("public_key"),
                                                   form_data.get("pre_key"),
                                                   form_data.get("signature"))
            return SuccessResponse()
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)

    async def get_public_keys(self, userId:str=None):
        try:
            return await self.key_service.get_public_keys(userId)
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)
    
    async def get_users(self, nickname:str):
        try:
            return await self.user_service.get_users(nickname)
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)
        
    async def get_messages(self, request:Request, chatId:str, offset:int=0):
        try:
            return await self.messenger_service.get_messages(request.state.user_id, chatId, offset)
        except UserNotInChat:
            raise HTTPException(detail="Доступ запрещен", status_code=403)
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)
    
    async def get_chat_data(self, chatId:str, request:Request):
        try:
            return await self.chat_service.get_chat_data(chatId, request.state.user_id)
        except UserNotInChat:
            raise HTTPException(detail="Доступ запрещен", status_code=403)
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)
        
    async def get_chat_type(self, chatId:str):
        try:
            return await self.chat_service.get_chat_type(chatId)
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)
        
    async def get_chat_members(self, chatId:str, request:Request):
        try:
            return await self.chat_service.get_chat_members(chatId, request.state.user_id)
        except UserNotInChat:
            raise HTTPException(detail="Доступ запрещен", status_code=403)
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)
    
    async def create_private_chat(self, request:Request, readerId:str):
        try:
            return await self.chat_service.create_private_chat(request.state.user_id, readerId)
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)
        
    async def get_chat_by_members(self, request:Request, readerId:str):
        try:
            return await self.chat_service.get_chat_by_members(request.state.user_id, readerId)
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)
    
    async def get_private_data(self, request:Request):
        try:
            return await self.user_service.get_user_data(request.state.user_id)
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)
        
    async def set_user_image(self, request:Request):
        try:
            form_data = await request.form()
            file_data = form_data.get("file")
            file_bytes = await file_data.read() if file_data else None

            if file_bytes:
                await self.user_service.set_user_image(request.state.user_id, file_bytes)

            return SuccessResponse()
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)
        
    async def set_user_name(self, request:Request):
        try:
            form_data = await request.form()
            await self.user_service.set_user_name(request.state.user_id, form_data.get("name"))
            return SuccessResponse()
        except TooShortName:
            raise HTTPException(detail=f"Имя слишком короткое", status_code=400)
        except EmptyName:
            raise HTTPException(detail="Не передано имя", status_code=400)
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)
        
    async def set_user_nickname(self, request:Request):
        try:
            form_data = await request.form()
            await self.user_service.set_user_nickname(request.state.user_id, form_data.get("nickname"))
            return SuccessResponse()
        except TooShortNickName:
            raise HTTPException(detail=f"Ник должен быть не короче {NICKNAME_MIN_LEN} символов", status_code=400)
        except EmptyNickname:
            raise HTTPException(detail="Не передан ник", status_code=400)
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)
    
    async def set_user_bio(self, request:Request):
        try:
            form_data = await request.form()
            await self.user_service.set_user_bio(request.state.user_id, form_data.get("bio"))
            return SuccessResponse()
        except TooLongBio:
            raise HTTPException(detail=f"Описание должно быть не больше {BIO_MAX_LEN} символов", status_code=400)
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)
        
    async def get_user_data(self, userId:str):
        try:
            return await self.user_service.get_user_data(userId)
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)
        
    async def get_chat_image(self, request:Request, chatId:str):
        try:
            image_bytes = await self.chat_service.get_chat_image(chatId, request.state.user_id)
            return Response(content=image_bytes, media_type="image/jpeg")
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)
        
    async def get_media_message(self, messageId:str, request:Request):
        try:
            return await self.messenger_service.get_media_message(request.state.user_id, messageId)
        
        except UnknownMessageType:
            raise HTTPException(detail="Неизвестный тип медиа сообщения", status_code=422)
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)
        
    async def get_user_image(self, userId:str):
        try:
            image_bytes = await self.user_service.get_user_image(userId)
            return Response(content=image_bytes, media_type="image/jpeg")
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)
        
    async def create_group_chat(self, request:Request):
        try:
            chat_id = await self.chat_service.create_group_chat(request.state.user_id)
            return {"chat_id":chat_id}
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)
        
    async def add_members(self, request:Request):
        try:
            form_data = await request.form()
            await self.chat_service.add_members(form_data.get("users_ids"), form_data.get("chat_id"))
            return SuccessResponse()
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=400)
        