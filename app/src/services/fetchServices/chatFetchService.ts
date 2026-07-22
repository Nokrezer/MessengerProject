import { userApi } from "@/src/settings/config"
import { authService } from "./authService";
import { fetchService, FetchService } from "./fetchService";

class ChatFetchService{
    private fetchService : FetchService;
    constructor(fetchService:FetchService){
        this.fetchService = fetchService;
    }

    async getChats(){
        const response = await this.fetchService.fetch({
            request:userApi.getChats, 
            method:"GET",
            headers:{
                Authorization: await authService.getAccessToken()
            }
        });
        
        return response;
    }

    async getChatData(chatId:string){
        const response = await this.fetchService.fetch({
            request:userApi.getChatData + "chatId=" + chatId,
            method:"GET",
            headers:{
                Authorization: await authService.getAccessToken()
            }
        });

        return response;
    }

    async createPrivateChat(readerId:string){
        const response = await this.fetchService.fetch(
            {request:userApi.createPrivateChat + "readerId=" + readerId,
            method:"POST",
            headers:{
                Authorization: await authService.getAccessToken()
            }
        });

        return response.chat_id;
    }

    async getChatByMembers(readerId:string){
        const response = await this.fetchService.fetch({
            request:userApi.getChatIdByMembers + "readerId=" + readerId,
            method:"GET",
            headers:{
                Authorization: await authService.getAccessToken()
            }
        });

        return response;
    }
}

export const chatFetchService = new ChatFetchService(fetchService);