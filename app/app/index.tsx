import {Text} from "react-native";
import { Redirect } from 'expo-router';
import { useLoadUserData } from '@/src/hooks/initHook';

export default function Index() {
  const { loading, userLogged } = useLoadUserData();
  
  if (loading) return <Text>Загрузка</Text>;
  
  return <Redirect href={userLogged ? '/(tabs)/chats' : '/(forms)/login'} />;
}