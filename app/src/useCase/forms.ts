import { authService } from "@/src/services/fetchServices/authService";
import {userService} from "@/src/services/fetchServices/userService";
import { accountStorageService } from "@/src/services/storageServices/accountStorageService";
import { tokenStorageService } from "@/src/services/storageServices/tokenStorageService";
import { showError } from '@/src/shared/appMessages';

import {router} from "expo-router";

export const loginButtonHandler = async (login:string, password:string) => {
    try{
      const [accessToken, refreshToken] = await authService.login(login, password);//входим в аккаунт
      //Делаем запрос на сервер и получаем id пользователя
      const userId = (await userService.getIdByToken(accessToken)).user_id;

      //сохраняем id пользователя и его токен
      await tokenStorageService.saveRefreshToken(userId, refreshToken);
      await accountStorageService.setNowAccountId(userId);//сохраняем аккаунт, который сейчас

      //Перенаправляем на страницу с вкладками
      router.push({pathname:"/chats"});
      }catch(error){
        showError(error);
      }
  };