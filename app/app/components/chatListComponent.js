import {View, Text} from "react-native";
import {Link} from "expo-router";

import { siteIp } from "@/src/settings/config";

export function ChatListComponent({chatDict}){
    return (<View>
        {chatDict.map((chatInfo => {
            return (
            <Link href={{pathname:"/chat/",
            params:{chatId:chatInfo.chat_id, title:chatInfo.title}
            }} key={chatInfo.chat_id}>
                <Text style={{color:"white"}}>{chatInfo.title}</Text>
            </Link>
            );
        }))}
    </View>)
}