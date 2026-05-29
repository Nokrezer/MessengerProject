import {SafeAreaProvider } from 'react-native-safe-area-context';
import { DarkTheme, DefaultTheme, ThemeProvider } from '@react-navigation/native';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import 'react-native-reanimated';

import { useColorScheme } from '@/hooks/use-color-scheme';
import {Text} from "react-native";
import Toast from 'react-native-toast-message';

import {useLoadUserData} from "@/src/hooks/initHook";

export const unstable_settings = {
  anchor: '(tabs)',
};

export default function RootLayout() {
  const colorScheme = useColorScheme();

  const {loading:loadingData, userLogged} = useLoadUserData();
  
  if(loadingData)
    return <Text>Загрузка</Text>;
  
  return (
    <SafeAreaProvider>
      <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
        <Stack
          screenOptions={{
          headerShown: false,  // Скрывает название страницв для ВСЕХ экранов в этом Stack
          }}>
        {userLogged ? <Stack.Screen name="(tabs)" options={{ headerShown: false }} /> :
        <Stack.Screen name="(forms)" options={{ headerShown: false }} />}
        </Stack>
        <StatusBar style="auto" />
                
        <Toast/>
      </ThemeProvider>
    </SafeAreaProvider>
  );
}
