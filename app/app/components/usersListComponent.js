import {Text, View, TouchableOpacity} from "react-native";
import {router} from "expo-router";
import { Image } from "expo-image";

import { useGlobalStyles } from "../styles/globalStyles";
import { useUserButtonStyle } from "../styles/userButtonStyle";

export function UsersListComponent({usersDict}){
    const globalStyles = useGlobalStyles();
    const userButtonStyle = useUserButtonStyle();
    
    return (<View>
        
        {usersDict.map(user => {
            
            return (
                <TouchableOpacity onPress={() => router.push({pathname:"/chat/", params:{readerId:user.user_id, title:user.name}})}
                key={user.user_id}>
                    <View style={userButtonStyle.chatButton}>
                        <Image source={{uri:user.imageUrl}} style={userButtonStyle.image}/>
                        
                        <View>
                            <Text style={[globalStyles.text, userButtonStyle.userName]}>{user.name}</Text>
                            <Text style={[globalStyles.text, userButtonStyle.nickname]}>@{user.nickname}</Text>
                        </View>
                    </View>
                </TouchableOpacity>
            );
        })}
    </View>);
}