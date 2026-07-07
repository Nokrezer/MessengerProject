from settings.config import *

from fastapi import WebSocket
import json

class RealTimeState():
    def __init__(self):
        self.authed_users = {}#id пользователя - вебсокет
        self.active_chats = {}#id чата - список активных пользователей(их id)

class RealTimeCore():
    def __init__(self, token_service, realtime_state, chat_database):
        self.token_service = token_service
        self.realtime_state = realtime_state
        self.chat_database = chat_database
        
    async def register_user(self, websocket:WebSocket):#регистрирует пользователя онлайн
        await websocket.accept()
        
        while True:
            try:
                data = await websocket.receive_text()
                json_message = json.loads(data)
                
                #нам нужно только зарегестрировать пользователя, поэтому получаем только access token
                if "ACCESS_TOKEN" in json_message:
                    token = json_message.get("ACCESS_TOKEN")
                    user_id = (await self.token_service.verify_access_token(token))["user_id"]

                    self.realtime_state.authed_users[user_id] = websocket
                    
                    #получаем id чатов в которых состоит пользователь
                    user_chats = await self.chat_database.get_user_chats(user_id)
                    for chat in user_chats:#перебираем чаты
                        chat_id = chat.get("chat_id")#получаем id чата
                        #пытаемся получить чат в словаре активных чатов
                        chat_exist = self.realtime_state.active_chats.get(chat_id)

                        if chat_exist:#если чат уже существовал, просто добавляем id пользователя
                            self.realtime_state.active_chats[chat_id].add(user_id)

                        elif not chat_exist:#если чата ранее не было, кэшируем
                            self.realtime_state.active_chats[chat_id] = {user_id}

                else:
                    await websocket.send_text("Ошибка регистрации")
            except Exception as e:
                await websocket.send_text("Ошибка регистрации")
        