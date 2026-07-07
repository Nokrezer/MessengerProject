import { authApi, userApi } from "@/src/settings/config.js";

import { Platform } from "react-native";

class AuthService{
    private accessToken;
    private refreshToken;

    constructor(){
        this.accessToken = "";
        this.refreshToken = "";
    }

    setRefreshToken(refreshToken:string){
        this.refreshToken = refreshToken;
    }

    async getAccessToken(){
        //При каждом получении токена проверяем его валидность
        const isVerifyed = await this.verifyAccessToken();
        
        //Если токен не валидный обновляем
        if(!isVerifyed)
            await this.updateAccessToken();
        
        return this.accessToken;
    }

    getRefreshToken(){
        return this.refreshToken;
        // return Platform.OS !== "web" ? this.refreshToken : null;
    }

    async verifyAccessToken(){
        if(!this.accessToken || this.accessToken === "")
            return false;

        const response = await fetch(authApi.verifyAccessToken, {
            method:"POST",
            headers:{
                Authorization: this.accessToken
            }
        });
        
        if(!response.ok)
            return false;

        return true;
    }

    async login(login:string, password:string){
        const form = new FormData();
        form.append("login", login);
        form.append("password", password);
        
        const response = await fetch(authApi.login, {
            credentials: "include",
            method: "POST",
            body: form
        });

        //Если код ошибка, выкидываем ошибку и передаём полученный словарь с данными об ошибке
        if(!response.ok)
            throw Error("Ошибка " + await response.text())
        
        //Если не веб, то сохраняем в память токены и возвращаем
        if(Platform.OS !== "web"){
            const {ACCESS_TOKEN, REFRESH_TOKEN} = await response.json();

            this.accessToken = ACCESS_TOKEN;
            this.refreshToken = REFRESH_TOKEN;
            
            return [ACCESS_TOKEN, REFRESH_TOKEN];
        }
        //Если веб, то токены сохранены в куки
        else
            return [null, null];
    }

    async updateAccessToken(){
        const response = await fetch(authApi.updateAccessToken, {
            method: "POST",
            headers:{
                Authorization:this.refreshToken
            }
        });

        if(!response.ok)
            throw Error("Ошибка " + await response.text())
        
        if(Platform.OS !== "web"){
            const {ACCESS_TOKEN} = await response.json();
            this.accessToken = ACCESS_TOKEN;
            
            return ACCESS_TOKEN;
        }
    }

    async verifyRefreshToken(){
        const response = await fetch(authApi.verifyRefreshToken, {
            method: "POST",
            headers:{
                Authorization:this.refreshToken
            }
        });

        if(!response.ok)
            throw Error("Ошибка " + await response.text())

        return true;
    }

    async requestAuthCode(email:string){
        const form = new FormData();
        form.append("email", email);

        const response = await fetch(authApi.requestAuthCode, {
            method:"POST",
            body:form
        })

        if(!response.ok)
            throw Error("Ошибка " + await response.text())
    }

    async requestRegCode(email:string){
        const form = new FormData();
        form.append("email", email);

        const response = await fetch(authApi.requestRegCode, {
            method:"POST",
            body:form
        })

        if(!response.ok)
            throw Error("Ошибка " + await response.text())
    }

    async loginWithCode(email:string, code:string){
        const form = new FormData();
        form.append("email", email);
        form.append("code", code);

        const response = await fetch(authApi.loginWithCode, {
            method:"POST",
            body:form
        });

        if(!response.ok)
            throw Error("Ошибка " + await response.text())
        
        //Если не веб, то сохраняем в память токены и возвращаем
        if(Platform.OS !== "web"){
            const {ACCESS_TOKEN, REFRESH_TOKEN} = await response.json();

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

        const response = await fetch(authApi.registration, {
            method:"POST",
            body:form
        });

        if(!response.ok)
            throw Error("Ошибка " + await response.text())
    }

    async getTempToken(){
        const refreshToken = this.getRefreshToken();

        const response = await fetch(authApi.getTempToken, {
            method:"POST",
            headers:{
                Authorization:refreshToken
            }
        });

        if(!response.ok)
            throw Error("Ошибка " + await response.text())
        
        const {TEMP_TOKEN} = await response.json()
        return TEMP_TOKEN;
    }
}

export const authService = new AuthService();