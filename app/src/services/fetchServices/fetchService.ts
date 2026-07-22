import { authApi } from "@/src/settings/config";
import { authService } from "./authService";

export class FetchService{
    async fetch({request, method, headers, body}:
        {request:string, method?:string, headers?:{}, body?:FormData}, isRetry=false):Promise<any>{
        const response = await fetch(request, {
                method:method ?? "GET",
                headers:{//'Accept-Encoding': 'gzip, deflate, br',
                ...headers},
                body:body
            });
            
        if(!response.ok){
            if(!isRetry && request !== authApi.updateAccessToken){//Если это первый запрос, то пытаемся обновить токен и сделать повторный запрос
                await authService.updateAccessToken();
                return await this.fetch({request, method, headers:{...headers, Authorization: await authService.getAccessToken()}, body}, true);
            }

            throw Error("Ошибка: " + (await response.text()));
        }

        try{
            return await response.json();
        }catch{}
    }
}

export const fetchService = new FetchService();