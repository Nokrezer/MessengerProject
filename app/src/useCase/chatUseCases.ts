import { ChatSession } from "./chatSession";
import { messageFetchService } from "../services/fetchServices/messagesFetchService";
import { showError } from "../shared/appMessages";
import { accountStorageService } from "../services/storageServices/accountStorageService";
import { userApi } from "../settings/config";

import { File } from 'expo-file-system';
import {router} from "expo-router";

import { fromUint8Array, toUint8Array } from "js-base64";

import {
  useAudioRecorder,
  AudioModule,
  RecordingPresets,
  setAudioModeAsync,
  useAudioRecorderState,
  useAudioPlayer,
  AudioRecorder,
  AudioPlayer
} from 'expo-audio';
import { authService } from "../services/fetchServices/authService";
import { preKeyStorageService } from "../services/storageServices/preKeyStorageService";

export const chatsSessions:Record<string, ChatSession> = {};//id чата/пользователя и объект сессии

async function sendMessageHandler(messageType:string, text?:any, data?:any, chatId?:string, readerId?:string, setText?:Function | null, setChatId?:Function){
    if(setText)
        setText("");
    
    let chatSession = chatsSessions[chatId as string];
    if(!chatSession){
        chatSession = new ChatSession(chatId, readerId);
        
        await chatSession.initData();

        if(chatId)
            chatsSessions[chatId] = chatSession;
    }
    
    chatId = await chatSession.sendMessage(messageType, text, data) as string;
    
    if(setChatId)
        setChatId(chatId);

    if(readerId)
        chatsSessions[chatId as string] = chatSession;
}

export async function sendTextMessageHandler(text:string, chatId?:string, readerId?:string, setText?:Function, setChatId?:Function) {
    await sendMessageHandler("text",text, null, chatId, readerId, setText, setChatId);
}

export async function sendVoiceMessageHandler(recorder:AudioRecorder, chatId?:string, readerId?:string, setChatId?:Function){
    await recorder.stop();
    
    const file = new File(recorder.uri as string);
    const fileBytes = await file.bytes();

    await sendMessageHandler("voice", null, fileBytes, chatId, readerId, null, setChatId);
}

export async function recordAudioHandler(recorder:AudioRecorder){
    await recorder.prepareToRecordAsync();
    recorder.record();
}

export async function stopRecordHandler(recorder:AudioRecorder){
    await recorder.stop();
}

//получает и расшифровывает медиа
async function getMediaMessage(message:{message_id:string, data:string, nonce:string}, chatId:string){
    const cryptedMessage = await messageFetchService.getMediaMessage(message.message_id);
    message = {...message, data:cryptedMessage};
    
    const chatSession = chatsSessions[chatId];
    const decryptedMessage = await chatSession.getMessage(message);
    if(decryptedMessage && "data" in decryptedMessage && decryptedMessage.data){
        const mediaBase64 = fromUint8Array(decryptedMessage.data as Uint8Array);
        const audioUri = `data:audio/wav;base64,${mediaBase64}`;
        return audioUri;
    }
    else
        return;
}

export async function playAudioMessage(player:AudioPlayer, message:{message_id:string, data:string, nonce:string}, chatId:string){
    const audioUri = await getMediaMessage(message, chatId);
    
    if(!audioUri)
        return;

    player.replace(audioUri);
    player.play();
}

//для подгрузки истории сообщений при заходе в чат
export async function getMessages(chatId:string){
        const history = await messageFetchService.getMessages(chatId);

        let chatSession = chatsSessions[chatId];
        if(!chatSession){
            chatSession = new ChatSession(chatId);
            chatsSessions[chatId] = chatSession;
        }
        
        await chatSession.initData();
        const userId = await accountStorageService.getNowAccountId();//Получаем id пользователя
        const keyId = await preKeyStorageService.getPublicKeyId(userId as string);
        
        const decryptedHistory = await Promise.all(history.map(async (message:{message_type:string, sender_id:string,
            text:string, message_id:string, nonce:string, key_id:string}) => {
                //если ключ шифрования сообщения не равен ключу который сейчас у клиента
                //задаём текст что сообщение не поддерживается
                if(keyId !== message.key_id){
                    return {
                        message_id: message.message_id,
                        display_info:"Сообщение недоступно",
                        message_type:"info",
                        is_my_message: message.sender_id === userId
                    };
                }
                
                return {
                ...message,
                text: (await chatSession.getMessage(message) as {text:string}).text,
                is_my_message: message.sender_id === userId};
        }));
        alert(JSON.stringify(decryptedHistory));
        return decryptedHistory;
}

//для расшифровки одного сообщения(для режима реал тайм)
export async function getOneMessage(message:{text:string, message_type:string, is_my_message:boolean, sender_id:string, data:string, nonce:string, message_id:string}, chatId:string){
    const chatSession = chatsSessions[chatId];

    const decryptedMessage = await chatSession.getMessage(message);

    const userId = await accountStorageService.getNowAccountId();//Получаем id пользователя
    
    message.text = decryptedMessage?.text as string;
    message["is_my_message"] = message.sender_id === userId;
    
    return message;
}

export async function deleteMessageHandler(messageId:string){
    await messageFetchService.deleteMessage(messageId);
}

export async function editMessageHandler(text:string, messageId:string, chatId:string, setText:Function){
    setText("");
    const chatSession = chatsSessions[chatId];
    await chatSession.editMessage(text, messageId);
}