import {View, Text, TouchableOpacity} from "react-native";
import {Image} from "expo-image";
import { router } from "expo-router";

import { useGlobalStyles } from "../styles/globalStyles";

import {useUserButtonStyle} from "@/app/styles/userButtonStyle";

export function ChatListComponent({chatDict}){
    const globalStyles = useGlobalStyles();
    const userButtonStyle = useUserButtonStyle();

    return (<View>
        {chatDict.map((chatInfo => {
            return (
            <TouchableOpacity onPress={() => router.push({pathname:"/chat/", params:{chatId:chatInfo.chat_id, title:chatInfo.title}})}
             key={chatInfo.chat_id} style={userButtonStyle.chatButton}>
                
                <Image style={userButtonStyle.image} source={{uri:chatInfo.imageUrl}}/>
                <Text style={[globalStyles.text, userButtonStyle.userName]}>{chatInfo.title || "Пользователь не найден"}</Text>
            </TouchableOpacity>
            );
        }))}
    </View>)
}