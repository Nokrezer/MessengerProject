import {tokenStorageService} from "@/src/services/storageServices/tokenStorageService";
import {accountStorageService} from "@/src/services/storageServices/accountStorageService";
import {authService} from "@/src/services/fetchServices/authService";
import { useState } from "react";
import { showError } from "../shared/appMessages";
import { chatStateStorageService } from "../services/storageServices/chatStateStorageService";

//Функция для загрузки всех данных с прошлых сессий(если такие есть) при открытии приложения
export async function loadUserData(){
    // await tokenStorageService.deleteAllTokens();
    try{
        //Получаем id аккаунта, в котором был последний вход(если таковой имеется)
        const nowAccountId = await accountStorageService.getNowAccountId();
        if(!nowAccountId)//Если таких данных нет
            return false;
        
        const nowAccountToken = await tokenStorageService.getRefreshToken(nowAccountId);

        //Передаём токен в сервис авторизации, для дальнейшей работы с ним
        authService.setRefreshToken(nowAccountToken);
        
        const verifyRefresh = await authService.verifyRefreshToken();//Проверяем, действительный ли токен

        return verifyRefresh;
    }catch{
    }
}