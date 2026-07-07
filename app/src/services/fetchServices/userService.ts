import { authApi, userApi } from "@/src/settings/config";
import { authService } from "./authService";

class UserService{
    async getIdByToken(accessToken: string){
        const response = await fetch(userApi.getIdByToken, {
            method: "GET",
            headers:{"Authorization":accessToken}
        });

        if(!response.ok)
            throw Error("Ошибка", {cause: await response.json()})

        return await response.json();
    }

    async getUsers(nickname:string){
        const response = await fetch(userApi.getUsers + "nickname=" + nickname, {
            headers:{
                Authorization: await authService.getAccessToken()
            }
        });

        if(!response.ok)
            throw Error("Ошибка", {cause: await response.json()})

        return await response.json();
    }

    async getPrivateData(){
        const response = await fetch(userApi.getPrivateData, {
            headers:{
                Authorization: await authService.getAccessToken()
            }
        });

        if(!response.ok)
            throw Error("Ошибка", {cause: await response.json()})

        return await response.json();
    }

    async getUserImage(userId:string){
        const tempToken = await authService.getTempToken();
        const response = await fetch(userApi.getUserImage + "userId=" + userId, {
            headers:{
                Authorization: tempToken
            }
        });

        if(!response.ok)
            throw Error("Ошибка", {cause: await response.json()})

        return await response.text();
    }

    async setUserImage(dir:string){
        const form = new FormData();
        form.append("file", {
                    uri: dir,
                    type: 'image/jpeg',
                    name: "image",
                } as any);
        
        const response = await fetch(userApi.setUserImage, {
            method:"POST",
            headers:{
                Authorization: await authService.getAccessToken()
            },
            body: form
        });

        if(!response.ok)
            throw Error("Ошибка", {cause: await response.json()})
    }

    async setUserName(name:string){
        const form = new FormData();
        form.append("name", name);
        
        const response = await fetch(userApi.setUserName, {
            method:"POST",
            headers:{
                Authorization: await authService.getAccessToken()
            },
            body: form
        });

        if(!response.ok)
            throw Error("Ошибка", {cause: await response.json()})
    }

    async setUserNickname(nickname:string){
        const form = new FormData();
        form.append("nickname", nickname);
        
        const response = await fetch(userApi.setUserNickname, {
            method:"POST",
            headers:{
                Authorization: await authService.getAccessToken()
            },
            body: form
        });

        if(!response.ok)
            throw Error("Ошибка", {cause: await response.json()})
    }

    async setUserBio(bio:string){
        const form = new FormData();
        form.append("bio", bio);
        
        const response = await fetch(userApi.setUserBio, {
            method:"POST",
            headers:{
                Authorization: await authService.getAccessToken()
            },
            body: form
        });

        if(!response.ok)
            throw Error("Ошибка", {cause: await response.json()})
    }
}

export const userService = new UserService();