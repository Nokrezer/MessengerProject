import { userApi } from "@/src/settings/config";
import { authService } from "./authService";
import { fetchService, FetchService } from "./fetchService";

class MessagesFetchService{
    private fetchService : FetchService;
    constructor(fetchService:FetchService){
        this.fetchService = fetchService;
    }

    async sendMessage(messageType:string, nonce:string, keyVersion:string, text?:string | null, data?:string | null, chatId?:string, readerId?:string){
        const form = new FormData();
        if(text)
            form.append("text", text);
        if(data)
            form.append("data", data);
        form.append("nonce", nonce);
        form.append("message_type", messageType);
        form.append(chatId ? "chat_id" : "reader_id", chatId ?? readerId ?? "");
        form.append("key_version", keyVersion);

        await this.fetchService.fetch({request:userApi.sendMessage, 
            method:"POST",
            headers:{
                Authorization: await authService.getAccessToken()
            },
            body:form
        });
    }

    async getMessages(chatId?:string, readerId?:string){
        const toId = chatId ? "chatId=" + chatId : "readerId=" + readerId
        const response = await this.fetchService.fetch({
            request:userApi.getMessages + toId,
            method:"GET",
            headers:{
                Authorization: await authService.getAccessToken()
            }
        });

        return response;
    }

    async getMediaMessage(messageId:string){
        const tempToken = await authService.getTempToken();

        const response = await this.fetchService.fetch({
            request:userApi.getMediaMessage + "messageId=" + messageId,
            headers:{
                Authorization: tempToken
            }
        });

        return response.media;
    }

    async editMessage(text:string, nonce:string, messageId:string){
        const form = new FormData();
        form.append("text", text);
        form.append("nonce", nonce);
        form.append("message_id", messageId);

        await this.fetchService.fetch({
            request:userApi.editMessage,
            method:"POST",
            body:form,
            headers:{
                Authorization: await authService.getAccessToken()
            }
        });
    }

    async deleteMessage(messageId:string){
        await this.fetchService.fetch({
            method:"DELETE",
            request:userApi.deleteMessage + "messageId=" + messageId,
            headers:{
                Authorization: await authService.getAccessToken()
            }
        });
    }
}

export const messageFetchService = new MessagesFetchService(fetchService);