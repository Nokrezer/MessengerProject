class UserService():
    def __init__(self, token_service, user_database):
        self.token_service = token_service
        self.user_database = user_database

    #Получение данных пользователя по его id
    async def get_user_data(self, user_id):
        # user_id = self.token_service.decrypt_token(token)["user_id"]
        return await self.user_database.get_user_by_id(user_id)
    
    #Получение 
    # async def get_user_id_by_token(self, token):

    