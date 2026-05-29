import {StyleSheet, useColorScheme, TextInput, Text, View, Button} from 'react-native';
import {SafeAreaView} from "react-native-safe-area-context";
import {useState} from "react";

import { loginButtonHandler } from '@/src/useCase/forms';

import {globalStyles} from "@/app/styles/global";

export default function LoginForm() {
  const [loginValue, setLogin] = useState("");
  const [passwordValue, setPassword] = useState("");

  return (
    <SafeAreaView>
      <View>
        <Text style={globalStyles.textColor}>Вход в аккаунт</Text>
        <TextInput style={[styles.textInput, globalStyles.textColor]} onChangeText={setLogin}></TextInput>
        <TextInput style={[styles.textInput, globalStyles.textColor]} onChangeText={setPassword}></TextInput>
        <Button title="send" onPress={() => loginButtonHandler(loginValue, passwordValue)}></Button>
        {/* <Button title="update access" onPress={updateToken} disabled={loading}></Button> */}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  textInput:{
    outline: "none",
    borderColor:"white",
  }
});
