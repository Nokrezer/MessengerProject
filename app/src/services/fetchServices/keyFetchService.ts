import { userApi } from "@/src/settings/config";
import { authService } from "./authService";

import { Base64 } from "js-base64";

class KeyFetchService{
    async sendPublicKeys(publicKey:Uint8Array, preKey:Uint8Array, signature:Uint8Array){
        const form = new FormData();
        form.append("public_key", Base64.fromUint8Array(publicKey));
        form.append("pre_key", Base64.fromUint8Array(preKey));
        form.append("signature", Base64.fromUint8Array(signature));

        const response = await fetch(userApi.sendPublicKeys, {
            method:"POST",
            headers:{
                Authorization: await authService.getAccessToken()
            },
            body:form
        });
    }

    async getPublicKeys(userId:string){
        const response = await fetch(userApi.getPublicKeys + "userId=" + userId, {
            headers:{
                Authorization: await authService.getAccessToken()
            }
        });

        if(!response.ok)
            throw Error("Ошибка", {cause: await response.json()})
        
        return await response.json();
    }
}

export const keyFetchService = new KeyFetchService();