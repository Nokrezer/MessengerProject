import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';
import { Base64 } from "js-base64";

class IdentKeyStorageService{
    async savePrivateKey(privateKey:Uint8Array, userId:string){
        if(Platform.OS !== "web"){
            const base64PrivateKey = Base64.fromUint8Array(privateKey);
            await SecureStore.setItemAsync(`privateIdentKey_${userId}`, base64PrivateKey);
        }
    }

    async savePublicKey(publicKey:Uint8Array, userId:string){
        if(Platform.OS !== "web"){
            const base64PublicKey = Base64.fromUint8Array(publicKey);
            await SecureStore.setItemAsync(`publicIdentKey_${userId}`, base64PublicKey);
        }
    }

    async getPublicKey(userId:string){
        if(Platform.OS !== "web"){
            const publicKey = await SecureStore.getItemAsync(`publicIdentKey_${userId}`);
            if(!publicKey)
                return null;
            
            return Base64.toUint8Array(publicKey);
        }
    }

    async getPrivateKey(userId:string){
        if(Platform.OS !== "web"){
            const privateKey = await SecureStore.getItemAsync(`privateIdentKey_${userId}`);
            if(!privateKey)
                return null;

            return Base64.toUint8Array(privateKey);
        }
    }

    async deletePublicKey(userId:string){
        await SecureStore.setItemAsync(`publicIdentKey_${userId}`, "");
    }

    async deletePrivateKey(userId:string){
        await SecureStore.setItemAsync(`privateIdentKey_${userId}`, "");
    }
}

export const identKeyStorageService = new IdentKeyStorageService();