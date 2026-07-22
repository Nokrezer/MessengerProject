import { userApi } from "@/src/settings/config";
import { authService } from "./authService";
import { fetchService, FetchService } from "./fetchService";

import { Base64 } from "js-base64";

class KeyFetchService{
    private fetchService : FetchService;
    constructor(fetchService:FetchService){
        this.fetchService = fetchService;
    }

    async sendPublicKeys(publicKey:Uint8Array, preKey:Uint8Array, signature:Uint8Array){
        const form = new FormData();
        form.append("public_key", Base64.fromUint8Array(publicKey));
        form.append("pre_key", Base64.fromUint8Array(preKey));
        form.append("signature", Base64.fromUint8Array(signature));

        const response = await this.fetchService.fetch({
            request:userApi.sendPublicKeys, 
            method:"POST",
            headers:{
                Authorization: await authService.getAccessToken()
            },
            body:form
        });
        alert(JSON.stringify(response));
        return response.key_version;
    }

    async getPublicKeys(userId:string){
        const response = await this.fetchService.fetch({
            request:userApi.getPublicKeys + "userId=" + userId,
            headers:{
                Authorization: await authService.getAccessToken()
            }
        });

        return response;
    }

    async getKeysByVersion(userId:string, version:string){
        const response = await this.fetchService.fetch({
            request:`${userApi.getKeysByVersion}userId=${userId}&keyVersion=${version}`,
            headers:{
                Authorization: await authService.getAccessToken()
            }
        });

        return response;
    }
}

export const keyFetchService = new KeyFetchService(fetchService);