import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';
import { Base64 } from "js-base64";

class ChatStateStorageService{
    async saveState(chatId:string, sendIndex:string, recvIndex:string){
        if(Platform.OS !== "web"){
            await SecureStore.setItemAsync(`chatState_${chatId}`, JSON.stringify({sendIndex, recvIndex}));
        }
    }

    async getState(chatId:string){
        if(Platform.OS !== "web"){
            const chatState = await SecureStore.getItemAsync(`chatState_${chatId}`);
            
            return chatState ? JSON.parse(chatState) : chatState;
        }
    }
}

export const chatStateStorageService = new ChatStateStorageService();