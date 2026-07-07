class NotEnoughArguments(Exception): pass#Если клиент передал недостаточно аргументов при запросе
class UserWithEmailExist(Exception): pass#При попытке регистрации, если почта была зарегестрирована на другой аккаунт
class UserNotFound(Exception): pass#При попытке входа, не был найден аккаунт пользователя(или пользователь ввёл неверные данные)
class IncorrectPassword(Exception): pass#Если введён неверный пароль
class TokenNotExists(Exception): pass#Если токен не был найден в БД
class ChatNotExist(Exception): pass#Если чат не найден в БД
class NeedAccessToken(Exception): pass#Если в запрос был передан токен доступа, а нужен токен refresh
class NeedRefreshToken(Exception): pass#тоже что и прошлая ошибка, но наоборот
class NeedToken(Exception): pass#Если при запросе не был передан не один из токенов
class NeedChatOrUserId(Exception): pass#Если при отправке сообщения не был передан id чата или получателя
class EmptyName(Exception) : pass#Если при изменении имени было передано пустое имя
class TooShortName(Exception): pass #Если был передан слишком короткое имя
class EmptyNickname(Exception) : pass#Если при изменении ника было передано пустое имя
class TooShortNickName(Exception): pass #Если был передан слишком короткий ник
class TooLongBio(Exception): pass #Если было передано слишком большое описание профиля
class NeedEmail(Exception): pass#Если не передана почта, где ожидалось
class NeedAuthCode(Exception): pass#если не передан код для входа/регистрации, где ожидалось
class AuthCodeExpired(Exception): pass#срок действия кода авторизации истек
class AuthCodeNotFinded(Exception): pass#Если код не был найден в БД(или истек)
class NeedName(Exception): pass#если пользователь передал пустое имя(или сплошные пробелы)
class NeedPassword(Exception): pass#если пользователь передал пустой пароль
class NeedLogin(Exception): pass#если пользователь передал пустой логин(почту или ник)
class UserNotInChat(Exception): pass#Если пользователь не состоит в чате
class UnknownMessageType(Exception): pass#При запросе получить содержимое медиа сообщения передан неизвестный тип