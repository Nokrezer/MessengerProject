import { chatFetchService } from "../services/fetchServices/chatFetchService";
import { authService } from "../services/fetchServices/authService";
import { getMessages, getOneMessage } from "@/src/useCase/chatUseCases";
import { realTimeService } from "../services/fetchServices/realTimeService";

import { userApi } from "../settings/config";

import { useEffect, useState } from "react";

import { AudioModule } from "expo-audio";

import { showErrorText } from "../shared/appMessages";

export function useGetAudioPermission(){
    useEffect(() => {(async () => {
        const status = await AudioModule.requestRecordingPermissionsAsync();
        if (!status.granted) {
            showErrorText("Разрешение на использование микрофона отклонено");
        }
    })()}, []);
}

export function useGetChats(){
    const [loading, setLoading] = useState(true);
    const [chats, setChats] = useState();

    useEffect(() => {(async() => {
        const chats = await chatFetchService.getChats();
        const token = await authService.getTempToken();
        
        //для каждого чата получаем ссылку для фото чата(собеседника)
        for(const chat of chats){
            chat["imageUrl"] = userApi.getChatImage + "chatId=" + chat.chat_id + "&tempToken=" + token;
        }
        
        setChats(chats);  
        setLoading(false);
    })()}, []);
    
    return {chats, loading};
}

export function useMessageHistory(chatId:string, readerId:string){
    const [history, setHistory] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [chatId_, setChatId] = useState(chatId);
    
    useEffect(() => {(async () => {
        if(!readerId)
            return;
        
        const id = await chatFetchService.getChatByMembers(readerId);
        
        if(id)
            setChatId(id.chat_id);
    })()}, []);

    useEffect(() => {
        setChatId(chatId);
    }, [chatId]);
    
    useEffect(() => {(async () => {
        if(chatId_)
            try{
                const chatHistory = await getMessages(chatId_);
                setHistory(chatHistory);
            }catch{
                setHistory([]);
            }
        
    
        setLoading(false);
    })()}, [chatId_]);

    useEffect(() => {(async () => {
        await realTimeService.sendRegistration();
        
        realTimeService.websocket.onmessage = async (event) => {
            const message = JSON.parse(event.data.replace(/'/g, '"'));
                
            switch(message.action){
                case "send":
                    const decryptedMessageData = await getOneMessage(message, chatId_);
                    
                    setHistory(pastMessages => [
                    ...pastMessages,
                    decryptedMessageData
                ]);
                break;
                case "delete":
                    setHistory(pastMessages => [
                    ...pastMessages.filter(msg => msg.message_id !== message.message_id)]);
                break;
                case "edit":
                    const decryptedText = (await getOneMessage(message, chatId_)).text;
                    setHistory(pastMessages => { 
                        const findedMessage = pastMessages.find(msg => msg.message_id === message.message_id);
                        const index = pastMessages.indexOf(findedMessage);
                        const newHistory = [...pastMessages];
                        newHistory[index].text = decryptedText;
                        return newHistory;
                    });
                break;
            }
        };
    })()}, [chatId_]);
    
    return [history, loading];
}