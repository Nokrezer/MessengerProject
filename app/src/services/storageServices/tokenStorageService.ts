import * as SecureStore from 'expo-secure-store';
import { Platform } from "react-native";

class TokenStorageService{
    async saveRefreshToken(userId:string, refreshToken:string){
        if(Platform.OS !== "web"){
            //Получаем токены которые были сохранены ранее
            const refreshTokens = await SecureStore.getItemAsync("refreshTokens");
            
            //Если до этого были сохранены токены, то парсим в словарь,
            //если не было то создаём новый пустой словарь
            const jsonData = refreshTokens && refreshTokens !== "" ? JSON.parse(refreshTokens) : {};
            //Добавляем или изменяем значение, по id пользователя
            jsonData[userId] = refreshToken;

            await SecureStore.setItemAsync("refreshTokens", JSON.stringify(jsonData));
        }
    }

    async getRefreshTokens(){
        if(Platform.OS !== "web"){
            const rawRefreshTokens = await SecureStore.getItemAsync("refreshTokens");
            return rawRefreshTokens && rawRefreshTokens !== "" ? JSON.parse(rawRefreshTokens) : null;
        }
    }

    async deleteAllTokens(){
        if(Platform.OS !== "web")
            await SecureStore.setItemAsync("refreshTokens", "");
    }
}

export const tokenStorageService = new TokenStorageService();