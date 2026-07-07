class MessengerRealtimeService():
    def __init__(self, realtime_state):
        self.realtime_state = realtime_state

    async def send_message(self, chat_id, text, nonce, message_id, message_type, sender_id):
        user_ids = self.realtime_state.active_chats.get(chat_id)

        response = {"chat_id":chat_id, "text":text or "", "nonce":nonce,
                    "message_id":message_id, "message_type":message_type,
                    "sender_id":sender_id}
        
        if user_ids:
            for user_id in user_ids:
                websocket = self.realtime_state.authed_users.get(user_id)
                
                try:
                    await websocket.send_text(str(response))
                except:
                    del self.realtime_state.authed_users[user_id]
                    del self.realtime_state.active_chats[chat_id][user_id]