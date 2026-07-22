import {SafeAreaView} from 'react-native-safe-area-context';
import {StyleSheet, useColorScheme, Text, View} from 'react-native';

import { useGetChats } from '@/src/hooks/chatsHook';
import {ChatListComponent} from "@/app/components/chatListComponent";

// import { useRealTimeMessages } from '@/src/hooks/chatsHook';

export default function ChatsPage() {
  const colorScheme = useColorScheme();

  //Получаем список чатов пользователя
  const {chats, loading} = useGetChats();
  // useRealTimeMessages();
  if(loading)
    return <Text>Загрузка</Text>;

  return <ChatListComponent chatDict={chats}/>;
}