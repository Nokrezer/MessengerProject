import { authApi, userApi } from "@/src/settings/config.js";

import { Platform } from "react-native";
import {fetchService, FetchService} from "./fetchService";

class AuthService{
    private accessToken;
    private refreshToken;
    private fetchService;

    constructor(fetchService:FetchService){
        this.accessToken = "";
        this.refreshToken = "";
        this.fetchService = fetchService;
    }

    setRefreshToken(refreshToken:string){
        this.refreshToken = refreshToken;
    }

    async getAccessToken(){
        //При каждом получении токена проверяем его валидность
        // const isVerifyed = await this.verifyAccessToken();
        //Если токен не валидный обновляем
        // if(!isVerifyed)
            // await this.updateAccessToken();
        
        return this.accessToken;
    }

    getRefreshToken(){
        return this.refreshToken;
    }

    async verifyAccessToken(){
        if(!this.accessToken || this.accessToken === "")
            return false;

        try{
            await this.fetchService.fetch({
                request:authApi.verifyAccessToken, 
                method:"POST",
                headers:{
                    Authorization: this.accessToken
                }
            });
            return true;
        }catch(err){
            return false;
        }
    }

    async login(login:string, password:string){
        const form = new FormData();
        form.append("login", login);
        form.append("password", password);
        
        const response = await this.fetchService.fetch({
            request:authApi.login,
            // credentials: "include",
            method: "POST",
            body: form
        });
        
        //Если не веб, то сохраняем в память токены и возвращаем
        if(Platform.OS !== "web"){
            const {ACCESS_TOKEN, REFRESH_TOKEN} = response;

            this.accessToken = ACCESS_TOKEN;
            this.refreshToken = REFRESH_TOKEN;
            
            return [ACCESS_TOKEN, REFRESH_TOKEN];
        }
        //Если веб, то токены сохранены в куки
        else
            return [null, null];
    }

    async updateAccessToken(){
        const response = await this.fetchService.fetch({
            request:authApi.updateAccessToken,
            method: "POST",
            headers:{
                Authorization:this.refreshToken
            }
        });
        
        if(Platform.OS !== "web"){
            this.accessToken = response.ACCESS_TOKEN;
            
            return this.accessToken;
        }
    }

    async verifyRefreshToken(){
        try{
            await this.fetchService.fetch({
                request:authApi.verifyRefreshToken, 
                method: "POST",
                headers:{
                    Authorization:this.refreshToken
                }
            });
            return true;
        }catch{
            return false;
        }
    }

    async requestAuthCode(email:string){
        const form = new FormData();
        form.append("email", email);

        await this.fetchService.fetch({
            request:authApi.requestAuthCode,
            method:"POST",
            body:form
        });
    }

    async requestRegCode(email:string){
        const form = new FormData();
        form.append("email", email);

        await this.fetchService.fetch({
            request:authApi.requestRegCode,
            method:"POST",
            body:form
        });
    }

    async loginWithCode(email:string, code:string){
        const form = new FormData();
        form.append("email", email);
        form.append("code", code);

        const response = await this.fetchService.fetch({
            request:authApi.loginWithCode,
            method:"POST",
            body:form
        });
        
        //Если не веб, то сохраняем в память токены и возвращаем
        if(Platform.OS !== "web"){
            const {ACCESS_TOKEN, REFRESH_TOKEN} = response;

            this.accessToken = ACCESS_TOKEN;
            this.refreshToken = REFRESH_TOKEN;
            
            return [ACCESS_TOKEN, REFRESH_TOKEN];
        }
        //Если веб, то токены сохранены в куки
        else
            return [null, null];
    }

    async registration(email:string, code:string, name:string, password:string){
        const form = new FormData();
        form.append("email", email);
        form.append("code", code);
        form.append("name", name);
        form.append("password", password);

        await this.fetchService.fetch({
            request:authApi.registration,
            method:"POST",
            body:form
        });
    }

    async getTempToken(){
        const response = await this.fetchService.fetch({
            request:authApi.getTempToken,
            method:"POST",
            headers:{
                Authorization: this.getRefreshToken()
            }
        });

        return response.TEMP_TOKEN;
    }
}

export const authService = new AuthService(fetchService);