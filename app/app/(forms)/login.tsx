import {StyleSheet, useColorScheme, TextInput, Text, View, TouchableOpacity} from 'react-native';
import {SafeAreaView} from "react-native-safe-area-context";
import {useState} from "react";
import {router} from "expo-router";

import { loginButtonHandler } from '@/src/useCase/forms';
//стили
import {useGlobalStyles, globalColors} from "@/app/styles/globalStyles";
import {useFormStyle} from "@/app/styles/formStyle";

export default function LoginForm() {
  const [loginValue, setLogin] = useState("");
  const [passwordValue, setPassword] = useState("");

  const globalStyles = useGlobalStyles();
  const formStyle = useFormStyle();

  return (
    <SafeAreaView>
      <View style={formStyle.block}>
        <Text style={[globalStyles.text, formStyle.formText]}>Вход</Text>
        <TextInput placeholder='Ник или почта' style={formStyle.input} placeholderTextColor={globalColors.placeHolder} onChangeText={setLogin}></TextInput>
        <TextInput placeholder='Пароль' style={formStyle.input}  placeholderTextColor={globalColors.placeHolder} onChangeText={setPassword}></TextInput>
        
        <TouchableOpacity onPress={() => loginButtonHandler(loginValue, passwordValue, ()=>{
          //Перенаправляем на страницу с вкладками
          router.push({pathname:"/chats"});
        })} style={[formStyle.button, globalStyles.button]}>
          <Text style={globalStyles.text}>Войти</Text>
        </TouchableOpacity>

        <TouchableOpacity onPress={() => router.push({pathname:"/(forms)/loginWithCode"})} style={formStyle.secondaryButton}>
          <Text style={formStyle.secondaryText}>Вход по коду</Text>
        </TouchableOpacity>

        <TouchableOpacity onPress={() => router.push({pathname:"/(forms)/reg"})} style={formStyle.secondaryButton}>
          <Text style={formStyle.secondaryText}>Регистрация</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}
