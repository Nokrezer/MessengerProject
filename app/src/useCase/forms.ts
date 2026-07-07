import { authService } from "@/src/services/fetchServices/authService";
import {userService} from "@/src/services/fetchServices/userService";
import { accountStorageService } from "@/src/services/storageServices/accountStorageService";
import { tokenStorageService } from "@/src/services/storageServices/tokenStorageService";
import { identKeyStorageService } from "../services/storageServices/identKeyStorageService";
import { preKeyStorageService } from "../services/storageServices/preKeyStorageService";
import { showError } from '@/src/shared/appMessages';

import { keyFetchService } from "../services/fetchServices/keyFetchService";

import { getRandomValues } from 'expo-random';
import "react-native-get-random-values";
import nacl from "tweetnacl";

//общая логика входа и сохранения токенов и ключей на устройстве
async function loginSave(accessToken:string, refreshToken:string, onSuccess?:()=>void){
  //Делаем запрос на сервер и получаем id пользователя
      const userId = (await userService.getIdByToken(accessToken)).user_id;

      //сохраняем id пользователя и его токен
      await tokenStorageService.saveRefreshToken(userId, refreshToken);
      await accountStorageService.setNowAccountId(userId);//сохраняем аккаунт, который сейчас

      //Пытаемся получить любой ключ(если ранее были входы)
      const privatePreKey = await preKeyStorageService.getPrivateKey(userId);
      
      if(!privatePreKey){
        //Создаём новую пару ключей шифрования
        const identKeys = nacl.sign.keyPair();//Для подписи ключей чатов
        const preKeys = nacl.box.keyPair();//Для шифрования чатов
        const signature = nacl.sign.detached(preKeys.publicKey, identKeys.secretKey);//сама подпись

        //Сохранение ключей
        await identKeyStorageService.savePrivateKey(identKeys.secretKey, userId);
        await identKeyStorageService.savePublicKey(identKeys.publicKey, userId);
        await preKeyStorageService.savePrivateKey(preKeys.secretKey, userId);
        await preKeyStorageService.savePublicKey(preKeys.publicKey, userId);
        //Отправляем публичные ключи на сервер
        await keyFetchService.sendPublicKeys(identKeys.publicKey, preKeys.publicKey, signature);
      }
      
      //При успехе, если передана какая-либо логика
      if(onSuccess)
        onSuccess();
}

export async function loginButtonHandler(login:string, password:string, onSuccess?:()=>void){
    try{
      const [accessToken, refreshToken] = await authService.login(login, password);//входим в аккаунт
      
      await loginSave(accessToken, refreshToken, onSuccess);
      }catch(error){
        showError({error:error as Error});
      }
  };

export async function sendCodeHandler(email:string){
  try{
    await authService.requestAuthCode(email);
  }catch(error){
    showError({error:error as Error});
  }
}

export async function loginWithCodeHandler(email:string, code:string, onSuccess?:()=>void){
  const [accessToken, refreshToken] = await authService.loginWithCode(email, code);
  await loginSave(accessToken, refreshToken, onSuccess);
}

export async function registrationHandler(email:string, code:string, name:string, password:string, onSuccess?:()=>void){
  try{
    await authService.registration(email, code, name, password);
    const [accessToken, refreshToken] = await authService.login(email, password);
    
    await loginSave(accessToken, refreshToken, onSuccess);
  }catch(error){
    showError({error:error as Error});
  }
}

export async function sendRegCodeHandler(email:string){
  try{
    await authService.requestRegCode(email);
  }catch(error){
    showError({error:error as Error});
  }
}