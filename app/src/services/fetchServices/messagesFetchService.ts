import { userApi } from "@/src/settings/config";
import { authService } from "./authService";

class MessagesFetchService{
    async sendMessage(messageType:string, nonce:string, text?:string | null, data?:string | null, chatId?:string, readerId?:string){
        const form = new FormData();
        if(text)
            form.append("text", text);
        if(data)
            form.append("data", data);
        form.append("nonce", nonce);
        form.append("message_type", messageType);
        form.append(chatId ? "chat_id" : "reader_id", chatId ?? readerId ?? "");

        const response = await fetch(userApi.sendMessage, {
            method:"POST",
            headers:{
                Authorization: await authService.getAccessToken()
            },
            body:form
        });

        if(!response.ok)
            throw Error("Ошибка: " + await response.text());

        return await response.text();
    }

    async getMessages(chatId?:string, readerId?:string){
        const toId = chatId ? "chatId=" + chatId : "readerId=" + readerId
        const response = await fetch(userApi.getMessages + toId, {
            method:"GET",
            headers:{
                Authorization: await authService.getAccessToken()
            }
        });

        if(!response.ok)
            throw Error("Ошибка: " + await response.text());

        return await response.json();
    }

    async getMediaMessage(messageId:string){
        const tempToken = await authService.getTempToken();

        const response = await fetch(userApi.getMediaMessage + "messageId=" + messageId, {
            headers:{
                Authorization: tempToken
            }
        });

        if(!response.ok)
            throw Error("Ошибка: " + await response.text());

        return await response.text();
    }
}

export const messageFetchService = new MessagesFetchService();