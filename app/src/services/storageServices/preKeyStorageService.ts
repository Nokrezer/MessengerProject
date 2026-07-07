import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';
import { Base64 } from "js-base64";

class PreKeyStorageService{
    async getPrivateKey(userId:string){
        if(Platform.OS !== "web"){
            const privateKey = await SecureStore.getItemAsync(`PrivatePreKey_${userId}`);
            if(!privateKey)
                return null;

            return Base64.toUint8Array(privateKey);
        }
    }

    async deletePublicKey(userId:string){
        await SecureStore.setItemAsync(`PublicPreKey_${userId}`, "");
    }

    async deletePrivateKey(userId:string){
        await SecureStore.setItemAsync(`PrivatePreKey_${userId}`, "");
    }

    async savePrivateKey(privateKey:Uint8Array, userId:string){
        if(Platform.OS !== "web"){
            const base64PrivateKey = Base64.fromUint8Array(privateKey);
            await SecureStore.setItemAsync(`PrivatePreKey_${userId}`, base64PrivateKey);
        }
    }

    async savePublicKey(publicKey:Uint8Array, userId:string){
        if(Platform.OS !== "web"){
            const base64PublicKey = Base64.fromUint8Array(publicKey);
            await SecureStore.setItemAsync(`PublicPreKey_${userId}`, base64PublicKey);
        }
    }

    async getPublicKey(userId:string){
        if(Platform.OS !== "web"){
            const publicKey = await SecureStore.getItemAsync(`PublicPreKey_${userId}`);
            if(!publicKey)
                return null;
            
            return Base64.toUint8Array(publicKey);
        }
    }
}

export const preKeyStorageService = new PreKeyStorageService();