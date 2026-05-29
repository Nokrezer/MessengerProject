import {View, Text} from "react-native";
import {SafeAreaView} from 'react-native-safe-area-context';

import { useLocalSearchParams } from "expo-router";

import { globalStyles } from "../styles/global";
//{chatId, title}:{chatId:string, title:string}
export default function chatPage(){
    const {chatId, title} = useLocalSearchParams();//<{chatId: string, title:string}>();

    alert(chatId + " " + title);
    return (
        <SafeAreaView>
            <View>
                <Text style={globalStyles.textColor}>Test chat</Text>
            </View>
        </SafeAreaView>
    );
}