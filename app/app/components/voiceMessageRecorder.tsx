import {TouchableOpacity, Text, View} from "react-native";
import {useState} from "react";
//хендлеры
import {recordAudioHandler, sendVoiceMessageHandler, stopRecordHandler} from "@/src/useCase/chatUseCases";
//стили
import { useGlobalStyles, useNowColor } from "../styles/globalStyles";
import { chatStyles } from "../styles/chatStyle";

//иконки
import MaterialIcons from '@expo/vector-icons/MaterialIcons';
import AntDesign from '@expo/vector-icons/AntDesign';

//для работы с аудио
import {
  useAudioRecorder,
  RecordingPresets
} from 'expo-audio';

import { useGetAudioPermission } from "@/src/hooks/chatsHook";


export function VoiceMessageButton({chatId, readerId, setChatId}:{chatId?:string | null, readerId?:string | null, setChatId:Function}){
    const color = useNowColor();
    const globalStyles = useGlobalStyles();

    //При записи ГС изменяем состояние записи и цвет кнопки
    const [recording, setRecording] = useState(false);
    
    //Для записи голосовых
    const recorder = useAudioRecorder(RecordingPresets.HIGH_QUALITY);
    
    //Получение разрешения на использование микрофона
    useGetAudioPermission();

    return (<View style={globalStyles.rowContainer}>
                {recording ? 
                <TouchableOpacity style={[chatStyles.button, globalStyles.button]} onPress={async () => {
                    setRecording(false);
                    await sendVoiceMessageHandler(recorder, chatId as string, readerId as string, setChatId);
                    }}>
                    <AntDesign name="send" size={24} color={color}/>
                </TouchableOpacity>
                :
                <TouchableOpacity style={[chatStyles.button, globalStyles.button]} onPress={async () => {
                    setRecording(!recording);
                    await recordAudioHandler(recorder)}}>
                    <MaterialIcons name="keyboard-voice" size={24} color={color}/>
                </TouchableOpacity>
                }

                {recording && <TouchableOpacity style={[chatStyles.button, globalStyles.button]}
                onPress={async () => {setRecording(false);
                    stopRecordHandler(recorder);}}>
                    <MaterialIcons name="cancel" size={24} color="red"/>
                </TouchableOpacity>}
            </View>);
}