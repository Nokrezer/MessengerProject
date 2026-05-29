import { userApi } from "@/src/settings/config"
import { authService } from "./authService";

class ChatService{
    async getChats(){
        const response = await fetch(userApi.getChats, {
            method:"GET",
            headers:{
                Authorization: await authService.getAccessToken()
            }
        });
        //a
        if(!response.ok)
            throw Error("Ошибка", {cause: await response.json()})
        
        const data = await response.json();
        return data;
    }
}

export const chatService = new ChatService();