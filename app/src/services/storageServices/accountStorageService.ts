import * as SecureStore from 'expo-secure-store';
import { Platform } from "react-native";

class AccountStorageService{
    async setNowAccountId(userId:string){
        if(Platform.OS !== "web")
            await SecureStore.setItemAsync("nowAccount", userId);
    }

    async getNowAccountId(){
        if(Platform.OS !== "web")
            return await SecureStore.getItemAsync("nowAccount");
    }
    // async saveId(userId:string){
    //     if(Platform.OS !== "web"){
    //         //Получаем токены которые были сохранены ранее
    //         const usersId = await SecureStore.getItemAsync("usersId");
                    
    //         //Если до этого были сохранены id аккаунтов, то парсим в словарь,
    //         //если не было то создаём новый пустой массив
    //         const listData = usersId ? JSON.parse(usersId) : [];
    //         //Добавляем id если до этого не было
    //         if(!(userId in listData))
    //             listData.push(userId);
        
    //         await SecureStore.setItemAsync("usersId", JSON.stringify(listData));
    //     }
    // }
}

export const accountStorageService = new AccountStorageService();