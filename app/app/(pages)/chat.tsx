//react
import {View, Text, TextInput, TouchableOpacity, KeyboardAvoidingView} from "react-native";
import {SafeAreaView} from 'react-native-safe-area-context';
import {useState, useEffect} from "react";
import { useLocalSearchParams, Stack } from "expo-router";

//компоненты
import {MessagesComponent} from "@/app/components/messagesHistoryComponent";
import { VoiceMessageButton } from "../components/voiceMessageRecorder";

//стили
import { useGlobalStyles, useNowColor } from "../styles/globalStyles";
import {chatStyles} from "@/app/styles/chatStyle";

//хендлеры
import { editMessageHandler, sendTextMessageHandler } from "@/src/useCase/chatUseCases";

//хуки
import { useMessageHistory } from "@/src/hooks/chatsHook";

//иконки
import AntDesign from '@expo/vector-icons/AntDesign';
import Entypo from '@expo/vector-icons/Entypo';

export default function ChatPage(){
    //стили
    const globalStyles = useGlobalStyles();
    const color = useNowColor();

    const [message, setMessage] = useState("");//Для отправки сообщений
    const [messageEditId, setMessageEditId] = useState<string | null>();//указывает, изменяет ли пользователь сейчас сообщение(его id) или просто null
    const {chatId, title, readerId} = useLocalSearchParams();//Из строки запроса берем аргументы
    const [chatId_, setChatId] = useState<string | null>(chatId as string);
    
    const [history, loading] = useMessageHistory(chatId_ as string, readerId as string);//Загрузка истории сообщений

    if(loading)
        return <Text>Загрузка</Text>;

    const sendMessageHandler = async () => {
        messageEditId ?
        await editMessageHandler(message, messageEditId as string, chatId_ as string, setMessage) :
        await sendTextMessageHandler(message, chatId_ as string, readerId as string, setMessage, setChatId);
        setMessageEditId(null);
    };
    
    return (
        <SafeAreaView edges={["bottom", "left", "right"]} style={{flex:1}}>
            <KeyboardAvoidingView style={{flex:1}}>
                <Stack.Screen options={{title:title as string}}/>

                <MessagesComponent setMessage={setMessage} setMessageEditId={setMessageEditId} messages={history} chatId={chatId_}/>

                <View>
                    {messageEditId ? <View style={[globalStyles.rowContainer, chatStyles.aboveMenu]}>
                            <Text style={globalStyles.text}>Редактирование</Text>
                            <TouchableOpacity style={{marginLeft:"auto"}} onPress={() => {
                                setMessageEditId(null);
                                setMessage("");
                            }}>
                                <Entypo name="cross" size={24} color={color}/>
                            </TouchableOpacity>
                    </View> : null}
                    <View style={[chatStyles.sendMessageBar, globalStyles.rowContainer]}>
                        <TextInput style={[globalStyles.input, chatStyles.input]} onChangeText={setMessage} value={message}/>
                        
                        {message && <TouchableOpacity style={[globalStyles.button, chatStyles.button]}
                        onPress={async () => await sendMessageHandler()}>
                            <AntDesign name="send" size={24} color={color}/>
                        </TouchableOpacity>}

                        {!message && <VoiceMessageButton chatId={chatId_} readerId={readerId as string} setChatId={setChatId}/>}
                    </View>
                </View>
            </KeyboardAvoidingView>
        </SafeAreaView>
    );
}