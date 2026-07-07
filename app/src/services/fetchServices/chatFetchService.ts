import { userApi } from "@/src/settings/config"
import { authService } from "./authService";

class ChatFetchService{
    async getChats(){
        const response = await fetch(userApi.getChats, {
            method:"GET",
            headers:{
                Authorization: await authService.getAccessToken()
            }
        });
        
        if(!response.ok)
            throw Error("Ошибка", {cause: await response.json()})
        
        return await response.json();
    }

    async getChatData(chatId:string){
        const response = await fetch(userApi.getChatData + "chatId=" + chatId, {
            method:"GET",
            headers:{
                Authorization: await authService.getAccessToken()
            }
        });

        if(!response.ok)
            throw Error("Ошибка", {cause: await response.json()})

        return await response.json();
    }

    async createPrivateChat(readerId:string){
        const response = await fetch(userApi.createPrivateChat + "readerId=" + readerId, {
            method:"POST",
            headers:{
                Authorization: await authService.getAccessToken()
            }
        });

        if(!response.ok)
            throw Error("Ошибка", {cause: await response.json()})

        return await response.json();
    }

    async getChatByMembers(readerId:string){
        const response = await fetch(userApi.getChatIdByMembers + "readerId=" + readerId, {
            method:"GET",
            headers:{
                Authorization: await authService.getAccessToken()
            }
        });

        if(!response.ok)
            throw Error("Ошибка", {cause: await response.json()})

        return await response.json();
    }
}

export const chatFetchService = new ChatFetchService();