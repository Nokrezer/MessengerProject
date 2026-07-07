//react
import {View, Text, TextInput, TouchableOpacity} from "react-native";
import {SafeAreaView} from 'react-native-safe-area-context';
import { useState } from "react";
//Стили
import { useGlobalStyles, useNowColor, globalColors } from "../styles/globalStyles";
import {userSearchStyle} from "@/app/styles/userSearchStyle";
//Компоненты
import {UsersListComponent} from "@/app/components/usersListComponent";

//Хендлеры
import { searchUsersHandler } from "@/src/useCase/users";

export default function ChatPage(){
    const globalStyles = useGlobalStyles();
    const [users, setUsers] = useState([]);

    return (
        <View>
            <TextInput style={[globalStyles.input, userSearchStyle.input]} placeholder="Ник пользователя" autoCapitalize="none"
            onChangeText={async (text) => setUsers(await searchUsersHandler(text))} placeholderTextColor={globalColors.placeHolder}></TextInput>
            
            <UsersListComponent usersDict={users}/>
        </View>
    );
}