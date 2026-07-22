class LogDatabase():
    def __init__(self, database):
        self.database = database
    
    async def add_error(self, action, error):
        await self.database.create("""INSERT INTO error_logs(action, error)
                                     VALUES(%s, %s)""", action, error)