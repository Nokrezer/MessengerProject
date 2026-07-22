import { messageFetchService } from "../services/fetchServices/messagesFetchService";
import { cryptService } from "../services/cryptService";
import { preKeyStorageService } from "../services/storageServices/preKeyStorageService";
import { accountStorageService } from "../services/storageServices/accountStorageService";
import { keyFetchService } from "../services/fetchServices/keyFetchService";
import { chatFetchService } from "../services/fetchServices/chatFetchService";
import { chatStateStorageService } from "../services/storageServices/chatStateStorageService";

import { showError } from "../shared/appMessages";

import { fromUint8Array, toUint8Array } from "js-base64";

import nacl from "tweetnacl";

import {ChatTypes} from "@/src/shared/types";

class ChatData{
    public chatId: string | null;
    public chatType: string | null;
    //readerId получается и храниться только если это личный чат
    public readerId: string | null;

    constructor(chatId?:string, readerId?:string){
        this.chatId = chatId || null;
        this.readerId = readerId || null;
        this.chatType = "private";
    }
}

export class ChatSession{
    public chatData: ChatData;
    private publicIdentKey: Uint8Array | null;//Публичный ключ собеседника
    private privatePreKey: Uint8Array | null;
    private sharedKey: Uint8Array | null;
    private sessionKey: Uint8Array | null;
    private publicPreKey: Uint8Array | null;
    private signature: Uint8Array | null;
    private keyVersions: {[version:string]:Uint8Array};
    private chatKey: Uint8Array | null;
    private nowKeyVersion: string | null;

    constructor(chatId?:string, readerId?:string){
        this.chatData = new ChatData(chatId, readerId);
        //ключи собеседника
        this.publicPreKey = null;
        this.publicIdentKey = null;
        this.signature = null;
        //ключи пользователя
        this.privatePreKey = null;
        //Общие ключи
        this.sharedKey = null;
        this.sessionKey = null;
        this.chatKey = null;

        this.keyVersions = {};//Хранит версию ключа(собеседника) и chatkey, для расшифровки старых сообщений
        this.nowKeyVersion = null;//Версия ключа, которая используется на данном клиенте данного пользователя
    }

    //Неизменяемые данные(в этой сесси)
    async initData(){
        let chatData;//Данные о типе чата получаем только если передан chatId
        const nowAccountId = await accountStorageService.getNowAccountId();
        
        this.nowKeyVersion = await preKeyStorageService.getPublicKeyVersion(nowAccountId as string) as string;
        // alert(1)
        alert(this.nowKeyVersion);
        this.privatePreKey = await preKeyStorageService.getPrivateKey(nowAccountId || "") || null;//Получаем свой приватный ключ
        
        if(this.chatData.chatId){
            chatData = await chatFetchService.getChatData(this.chatData.chatId);
            this.chatData.chatType = chatData.chat_type;

            //Если тип чата оказался приватным, получаем id собеседника(если ранее не был получен)
            if(chatData.chat_type === ChatTypes.PRIVATE && !this.chatData.readerId)
                this.chatData.readerId = JSON.parse(chatData.user_ids).filter((userId:string) => userId !== nowAccountId)[0];
        }
        
        switch(this.chatData.chatType){
            case ChatTypes.PRIVATE:
                const publicKeys = await keyFetchService.getPublicKeys(this.chatData.readerId as string);
                const lastKeyVersion = publicKeys.key_version;
                this.publicIdentKey = toUint8Array(publicKeys.public_key);
                this.publicPreKey = toUint8Array(publicKeys.pre_key);
                this.signature = toUint8Array(publicKeys.signature);
                
                const verifiedPreKey = nacl.sign.detached.verify(this.publicPreKey as Uint8Array, this.signature as Uint8Array, this.publicIdentKey as Uint8Array);
                if(!verifiedPreKey){
                    showError({text:"Ошибка подписи ключей собеседника"});
                    return;
                }
                
                this.sharedKey = cryptService.sharedKey(this.publicPreKey as Uint8Array, this.privatePreKey as Uint8Array);
                this.chatKey = cryptService.KDF(this.sharedKey as Uint8Array, `chat_${this.chatData.chatId}`);

                this.keyVersions[lastKeyVersion] = this.sharedKey;
            break;
        }
    }

    private async addNewKeyVersion(keyVersion:string){
        const keys = await keyFetchService.getKeysByVersion(this.chatData.readerId as string, keyVersion);
        const sharedKey = cryptService.sharedKey(keys.publicPreKey as Uint8Array, keys.privatePreKey as Uint8Array);
        this.keyVersions[keyVersion] = sharedKey;
    }

    private async decryptMessage(text?:string, data?:any){
        if(!this.chatKey)
            this.chatKey = cryptService.KDF(this.sharedKey as Uint8Array, `chat_${this.chatData.chatId}`);
        
        const nonce = nacl.randomBytes(24);
        const base64Nonce = fromUint8Array(nonce);

        let base64Text = null;
        let base64Data = null;
        
        if(text){
            //Шифруем текст
            const cryptedText = cryptService.cryptMessage(text, nonce, this.chatKey);
            base64Text = fromUint8Array(cryptedText);
        }

        if(data){
            //Шифруем медиа
            const cryptedData = cryptService.cryptMediaMessage(data, nonce, this.chatKey);
            base64Data = fromUint8Array(cryptedData);
        }

        return {base64Text, base64Nonce, base64Data};
    }

    async editMessage(text:string, messageId:string){
        const {base64Text, base64Nonce} = await this.decryptMessage(text);

        await messageFetchService.editMessage(base64Text as string, base64Nonce, messageId);
    }

    async sendMessage(messageType:string, text?:string, data?:any){
        if(!this.chatData.chatId)//Если чат не создан - создаём
            this.chatData.chatId = await chatFetchService.createPrivateChat(this.chatData.readerId as string);
        
        const {base64Text, base64Nonce, base64Data} = await this.decryptMessage(text, data);
        //Отправляем соо на сервер
        // alert(this.nowKeyVersion);
        await messageFetchService.sendMessage(messageType, base64Nonce, this.nowKeyVersion as string, base64Text, base64Data, this.chatData.chatId as string);

        return this.chatData.chatId;
    }

    async getMessage(message:{text?:string, data?:string, nonce:string, key_version:string}){
        
        let messageText = null;
        let messageData = null;

        let nowChatkey = null;
        if(message.key_version !== this.nowKeyVersion)
            await this.addNewKeyVersion(message.key_version);
        
        // try{
        if(message.text != null){
            const decryptedText = cryptService.decryptMessage(toUint8Array(message.text), toUint8Array(message.nonce), this.keyVersions[message.key_version] as Uint8Array) as Uint8Array;
            messageText = new TextDecoder().decode(decryptedText);
        }
        if("data" in message && message.data)
            messageData = cryptService.decryptMessage(toUint8Array(message.data), toUint8Array(message.nonce), this.keyVersions[message.key_version] as Uint8Array) as Uint8Array;
        // }catch{
        //     return;
        // }
        const decryptedMessage = {text:messageText, data:messageData};
        
        return decryptedMessage;
    }
}