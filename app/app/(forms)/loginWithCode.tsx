import {View, TextInput, Text, TouchableOpacity} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import {router} from "expo-router";
import {useState} from "react";

import { useGlobalStyles, globalColors } from "../styles/globalStyles";
import { useFormStyle } from "../styles/formStyle";

import { sendCodeHandler, loginWithCodeHandler } from "@/src/useCase/forms";

export default function loginWithCodeForm(){
    const globalStyles = useGlobalStyles();
    const formStyle = useFormStyle();

    const [emailBtnDisabled, setEmailBtnDisabled] = useState(true);
    const [email, setEmail] = useState("");
    const [code, setCode] = useState("");

    return (<SafeAreaView>
        <View style={formStyle.block}>
            <Text style={[globalStyles.text, formStyle.formText]}>Вход по коду</Text>

            <TextInput style={formStyle.input} onChangeText={(text) => {setEmailBtnDisabled(false); setEmail(text)}}
            placeholder="Почта" placeholderTextColor={globalColors.placeHolder}></TextInput>

            <TextInput style={formStyle.input} onChangeText={(text) => {setEmailBtnDisabled(false); setCode(text)}}
            placeholder="Код из письма" placeholderTextColor={globalColors.placeHolder}></TextInput>

            <TouchableOpacity style={[globalStyles.button, formStyle.button]}
            onPress={() => {setEmailBtnDisabled(true); sendCodeHandler(email)}} disabled={emailBtnDisabled}>
                <Text style={globalStyles.text}>Отправить код</Text>
            </TouchableOpacity>

            <TouchableOpacity style={[globalStyles.button, formStyle.button]} onPress={() => loginWithCodeHandler(email, code, ()=>{
                //Перенаправляем на страницу с вкладками
                router.push({pathname:"/chats"});
            })}>
                <Text style={globalStyles.text}>Войти</Text>
            </TouchableOpacity>

            <TouchableOpacity onPress={() => router.push({pathname:"/(forms)/login"})} style={formStyle.secondaryButton}>
                      <Text style={formStyle.secondaryText}>Обычный вход</Text>
            </TouchableOpacity>
                    
            <TouchableOpacity onPress={() => router.push({pathname:"/(forms)/reg"})} style={formStyle.secondaryButton}>
                <Text style={formStyle.secondaryText}>Регистрация</Text>
            </TouchableOpacity>
        </View>
    </SafeAreaView>);
}