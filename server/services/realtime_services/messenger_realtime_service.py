from shared.types import RealTimeActions

class MessengerRealtimeService():
    def __init__(self, realtime_state):
        self.realtime_state = realtime_state

    #общий метод для отправки действий или сообщений клиентам по веб сокету
    async def _send(self, chat_id, response, sender_id):
        user_ids = self.realtime_state.active_chats.get(chat_id)

        #если в чате есть активные пользователи и отправитель тоже присутствует в чате
        if user_ids and sender_id in user_ids:
            for user_id in user_ids:
                websocket = self.realtime_state.authed_users.get(user_id)
                
                try:
                    await websocket.send_text(str(response))
                except:
                    del self.realtime_state.authed_users[user_id]
                    del self.realtime_state.active_chats[chat_id][user_id]

    async def send_message(self, chat_id, text, nonce, message_id, message_type, sender_id):
        response = {"chat_id":chat_id, "text":text or "", "nonce":nonce,
                    "message_id":message_id, "message_type":message_type,
                    "sender_id":sender_id, "action":RealTimeActions.SEND_MESSAGE}
        
        await self._send(chat_id, response, sender_id)
        
    async def delete_message(self, chat_id, message_id, sender_id):
        response = {"action":RealTimeActions.DELETE_MESSAGE, "chat_id":chat_id, "message_id":message_id}
        await self._send(chat_id, response, sender_id)
    
    async def edit_message(self, chat_id, message_id, sender_id, text, nonce):
        response = {"action":RealTimeActions.EDIT_MESSAGE, "chat_id":chat_id, "message_id":message_id,
                    "text":text, "nonce":nonce}
        await self._send(chat_id, response, sender_id)