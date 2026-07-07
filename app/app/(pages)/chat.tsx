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
import { sendTextMessageHandler } from "@/src/useCase/chatUseCases";

//хуки
import { useMessageHistory } from "@/src/hooks/chatsHook";

//иконки
import AntDesign from '@expo/vector-icons/AntDesign';

export default function ChatPage(){
    //стили
    const globalStyles = useGlobalStyles();
    const color = useNowColor();

    const [message, setMessage] = useState("");//Для отправки сообщений
    const {chatId, title, readerId} = useLocalSearchParams();//Из строки запроса берем аргументы
    const [chatId_, setChatId] = useState<string | null>(chatId as string);
    
    const [history, loading] = useMessageHistory(chatId_, readerId);//Загрузка истории сообщений
    
    if(loading)
        return <Text>Загрузка</Text>;
    
    return (
            <KeyboardAvoidingView>
                <Stack.Screen options={{title:title as string}}/>

                <MessagesComponent messagesDict={history} chatId={chatId_}/>

                <View style={[chatStyles.sendMessageBar, globalStyles.rowContainer]}>
                    <TextInput style={[globalStyles.input, chatStyles.input]} onChangeText={setMessage} value={message}/>
                    
                    {message && <TouchableOpacity style={[globalStyles.button, chatStyles.button]}
                    onPress={async () => await sendTextMessageHandler(message, chatId_ as string, readerId as string, setMessage, setChatId)}>
                        <AntDesign name="send" size={24} color={color}/>
                    </TouchableOpacity>}

                    {!message && <VoiceMessageButton chatId={chatId_} readerId={readerId as string} setChatId={setChatId}/>}
                </View>

            </KeyboardAvoidingView>
    );
}