import {Text, ScrollView, TouchableOpacity, View} from "react-native";

//стили
import { useGlobalStyles, useNowColor } from "../styles/globalStyles";
import { chatStyles } from "../styles/chatStyle";

import { playAudioMessage } from "@/src/useCase/chatUseCases";
//хуки
import { useAudioPlayer } from "expo-audio";
//иконки
import Entypo from '@expo/vector-icons/Entypo';
//прочее
import { MessagesTypes } from "@/src/shared/types";

export function MessagesComponent({messagesDict, chatId}){
    try{
        const globalStyles = useGlobalStyles();
        const color = useNowColor();

        const player = useAudioPlayer();
        
        return (
            <ScrollView style={[chatStyles.messagesView]}>
                {messagesDict.map(message => {
                    let mediaMessage = null;
                    //Проверка, является ли сообщение медиа
                    switch(message.message_type){
                        case MessagesTypes.VOICE:
                            mediaMessage = <TouchableOpacity style={[globalStyles.rowContainer, chatStyles.voiceMessage]}
                                                onPress={async () => await playAudioMessage(player, message, chatId)}>
                                                <Entypo name="controller-play" size={24} color={color}/>
                                                <Text style={globalStyles.text}>Голосовое сообщение</Text>
                                            </TouchableOpacity>;
                    }
                    
                    return (
                    <View key={message.message_id} style={[chatStyles.message, message.isMyMessage === true ? chatStyles.myMessage : null]}>
                        {mediaMessage}
                        {message.text ? <Text style={[globalStyles.text]}>{message.text}</Text> : null}
                    </View>
                    )
                })}
            </ScrollView>
        );
    }catch{}
}