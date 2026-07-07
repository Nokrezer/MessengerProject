import {View, TextInput, Text, TouchableOpacity} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import {router} from "expo-router";
import {useState} from "react";

import { useGlobalStyles, globalColors } from "../styles/globalStyles";
import { useFormStyle } from "../styles/formStyle";

import { registrationHandler, sendRegCodeHandler } from "@/src/useCase/forms";

export default function RegistrationForm(){
    const globalStyles = useGlobalStyles();
    const formStyle = useFormStyle();

    const [emailBtnDisabled, setEmailBtnDisabled] = useState(true);
    const [email, setEmail] = useState("");
    const [code, setCode] = useState("");
    const [password, setPassword] = useState("");
    const [name, setName] = useState("");

    return (<SafeAreaView>
        <View style={formStyle.block}>
            <Text style={[globalStyles.text, formStyle.formText]}>Регистрация</Text>

            <TextInput style={formStyle.input} onChangeText={(text) => {setEmailBtnDisabled(false); setEmail(text)}}
            placeholder="Почта" placeholderTextColor={globalColors.placeHolder}></TextInput>

            <TextInput style={formStyle.input} onChangeText={setName}
            placeholder="Имя" placeholderTextColor={globalColors.placeHolder}></TextInput>

            <TextInput style={formStyle.input} onChangeText={setPassword}
            placeholder="Пароль" placeholderTextColor={globalColors.placeHolder} secureTextEntry={true}></TextInput>

            <TextInput style={formStyle.input} onChangeText={(text) => {setEmailBtnDisabled(false); setCode(text)}}
            placeholder="Код из письма" placeholderTextColor={globalColors.placeHolder}></TextInput>

            <TouchableOpacity style={[globalStyles.button, formStyle.button]}
            onPress={() => {setEmailBtnDisabled(true); sendRegCodeHandler(email)}} disabled={emailBtnDisabled}>
                <Text style={globalStyles.text}>Отправить код</Text>
            </TouchableOpacity>

            <TouchableOpacity style={[globalStyles.button, formStyle.button]} onPress={() => registrationHandler(email, code, name, password, ()=>{
                //Перенаправляем на страницу с вкладками
                router.push({pathname:"/chats"});
            })}>
                <Text style={globalStyles.text}>Зарегистрироваться</Text>
            </TouchableOpacity>

            <TouchableOpacity onPress={() => router.push({pathname:"/(forms)/login"})} style={formStyle.secondaryButton}>
                      <Text style={formStyle.secondaryText}>Обычный вход</Text>
            </TouchableOpacity>
                    
            <TouchableOpacity onPress={() => router.push({pathname:"/(forms)/loginWithCode"})} style={formStyle.secondaryButton}>
                <Text style={formStyle.secondaryText}>Вход по коду</Text>
            </TouchableOpacity>
        </View>
    </SafeAreaView>);
}