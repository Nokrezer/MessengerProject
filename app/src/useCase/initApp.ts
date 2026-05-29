import {tokenStorageService} from "@/src/services/storageServices/tokenStorageService";
import {accountStorageService} from "@/src/services/storageServices/accountStorageService";
import {authService} from "@/src/services/fetchServices/authService";

//Функция для загрузки всех данных с прошлых сессий(если такие есть) при открытии приложения
export async function loadUserData(){
    // await tokenStorageService.deleteAllTokens();
    //Получаем id аккаунта, в котором был последний вход
    const nowAccountId = await accountStorageService.getNowAccountId();
    //Получаем аккаунты в которые выполнен вход
    const refreshTokens = await tokenStorageService.getRefreshTokens();

    if(!refreshTokens)//Если нету никаких входов
        return false;

    const nowAccountToken = nowAccountId ? refreshTokens[nowAccountId] : null;//Ищем токен по id
    
    authService.setRefreshToken(nowAccountToken);
    await authService.getAccessToken();
    
    const verifyRefresh = await authService.verifyRefreshToken();//Проверяем, действительный ли токен

    return verifyRefresh;
}