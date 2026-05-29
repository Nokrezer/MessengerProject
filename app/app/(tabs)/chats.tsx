import {SafeAreaView} from 'react-native-safe-area-context';
import {StyleSheet, useColorScheme, Text, View} from 'react-native';

import { useGetChats } from '@/src/hooks/chatsHook';
import {ChatListComponent} from "@/app/components/chatListComponent";

export default function ChatsScreen() {
  const colorScheme = useColorScheme();
  const textColor = colorScheme === "dark" ? "white" : "black";

  //Получаем список чатов пользователя
  const {chats, loading} = useGetChats();
  
  if(loading)
    return <Text>Загрузка</Text>;

  return (
    <SafeAreaView>
        <View>
          <Text style={{color:textColor}}>Чаты</Text>
        </View>
        <ChatListComponent chatDict={chats}/>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  textInput:{
    outline: "none",
    borderColor:"white",
  },

  // button:{
    // color:
  // }
});
