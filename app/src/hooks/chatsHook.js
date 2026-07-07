import { chatFetchService } from "../services/fetchServices/chatFetchService";
import { authService } from "../services/fetchServices/authService";
import { getMessages, getOneMessage } from "@/src/useCase/chatUseCases";
import { realTimeService } from "../services/fetchServices/realTimeService";

import { userApi } from "../settings/config";

import { useEffect, useState } from "react";

import { AudioModule } from "expo-audio";

import { showError } from "../shared/appMessages";

export function useGetAudioPermission(){
    useEffect(() => {(async () => {
        const status = await AudioModule.requestRecordingPermissionsAsync();
        if (!status.granted) {
            showError("Разрешение на использование микрофона отклонено");
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

export function useMessageHistory(chatId, readerId){
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [chatId_, setChatId] = useState(chatId);
    
    useEffect(() => {(async () => {
        const id = await chatFetchService.getChatByMembers(readerId);
        
        if(id)
            setChatId(id.chat_id);
    })()}, []);

    useEffect(() => {
        setChatId(chatId);
    }, [chatId]);
    
    useEffect(() => {(async () => {
        if(chatId_){
            const chatHistory = await getMessages(chatId_);
            setHistory(chatHistory);
        }
    
        setLoading(false);
    })()}, [chatId_]);

    useEffect(() => {(async () => {
        await realTimeService.sendRegistration();
        
        realTimeService.websocket.onmessage = async (event) => {
            const message = JSON.parse(event.data.replace(/'/g, '"'));
            
            const decryptedMessageData = await getOneMessage(message, chatId_);
            
            setHistory(pastMessages => [
                ...pastMessages,
                decryptedMessageData
            ]);
        };
    })()}, [chatId_]);
    
    return [history, loading];
}