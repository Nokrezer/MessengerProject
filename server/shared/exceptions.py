class NotEnoughArguments(Exception): pass#Если клиент передал недостаточно аргументов при запросе
class UserWithEmailExist(Exception): pass#При попытке регистрации, если почта была зарегестрирована на другой аккаунт
class UserNotFound(Exception): pass#При попытке входа, не был найден аккаунт пользователя(или пользователь ввёл неверные данные)
class IncorrectPassword(Exception): pass#Если введён неверный пароль
class TokenNotExistsInDatabase(Exception): pass#Если токен не был найден в БД
class ChatNotExist(Exception): pass#Если чат не найден в БД
class NeedAccessToken(Exception): pass#Если в запрос был передан токен доступа, а нужен токен refresh
class NeedRefreshToken(Exception): pass#тоже что и прошлая ошибка, но наоборот
class NeedToken(Exception): pass#Если при запросе не был передан не один из токенов
class NeedChatOrUserId(Exception): pass#Если при отправке сообщения не был передан id чата или получателя