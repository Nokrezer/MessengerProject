import {Text, ScrollView, TouchableOpacity, View, Modal} from "react-native";
import {useState} from "react";

//стили
import { useGlobalStyles, useNowColor } from "../styles/globalStyles";
import { chatStyles } from "../styles/chatStyle";

import { playAudioMessage } from "@/src/useCase/chatUseCases";
//хуки
import { useAudioPlayer } from "expo-audio";
//иконки
import Entypo from '@expo/vector-icons/Entypo';
import FontAwesome from '@expo/vector-icons/FontAwesome';
import Feather from '@expo/vector-icons/Feather';
import MaterialCommunityIcons from '@expo/vector-icons/MaterialCommunityIcons';
//прочее
import { MessageTypes } from "@/src/shared/types";

import { deleteMessageHandler } from "@/src/useCase/chatUseCases";

function MessageMenu({setMessage, menuPos, setMenuPos, setMessageEditId, nowSelectedMessage}){
    const globalStyles = useGlobalStyles();
    const color = useNowColor();

    return (<>
        {menuPos ?
            <Modal transparent={true}>
                <TouchableOpacity style={{height:"100%", width:"100%"}} onPress={() => setMenuPos(null)}>

                    <View style={[chatStyles.messageMenu, {left:menuPos.x, top:menuPos.y}]}>
                        <TouchableOpacity style={[globalStyles.rowContainer, chatStyles.messageMenuButton]}
                        onPress={() => {
                            setMessageEditId(nowSelectedMessage.message_id);
                            setMenuPos(null);
                            setMessage(nowSelectedMessage.text);}}>
                                
                            <MaterialCommunityIcons name="pencil" size={24} color={color} />
                            <Text style={[globalStyles.text, chatStyles.messageMenuText]}>Изменить</Text>
                        </TouchableOpacity>

                        <TouchableOpacity onPress={async () => {
                            await deleteMessageHandler(nowSelectedMessage.message_id);
                            setMenuPos(null);}}
                            style={[globalStyles.rowContainer, chatStyles.messageMenuButton]}>
                            <Feather name="trash-2" size={24} color={color}/>
                            
                            <Text style={[globalStyles.text, chatStyles.messageMenuText]}>Удалить</Text>
                        </TouchableOpacity>
                    </View>
                </TouchableOpacity>
            </Modal> : null}
        </>);
}

export function MessagesComponent({setMessage, messages, chatId, setMessageEditId}){
    try{
        const globalStyles = useGlobalStyles();
        const color = useNowColor();

        const player = useAudioPlayer();
        
        const [menuPos, setMenuPos] = useState(null);
        const [nowSelectedMessage, setSelected] = useState();
        
        return (<>
            <MessageMenu setMessage={setMessage} menuPos={menuPos} setMenuPos={setMenuPos} setMessageEditId={setMessageEditId} nowSelectedMessage={nowSelectedMessage}/>

            <ScrollView style={[chatStyles.messagesView]}>
                
                {messages.map(message => {
                    let mediaMessage = null;
                    //Проверка, является ли сообщение медиа 
                    switch(message.message_type){
                        case MessageTypes.VOICE:
                            mediaMessage = <TouchableOpacity style={[globalStyles.rowContainer, chatStyles.voiceMessage]}
                                                onPress={async () => await playAudioMessage(player, message, chatId)}>
                                                <Entypo name="controller-play" size={24} color={color}/>
                                                <Text style={globalStyles.text}>Голосовое сообщение</Text>
                                            </TouchableOpacity>;
                        break;
                        case MessageTypes.INFO:
                            mediaMessage = <Text style={[globalStyles.text]}>{message.display_info} <FontAwesome name="exclamation-triangle" size={15} color={color} /></Text>
                        break;
                    }
                    
                    return (<View key={message.message_id}>
                            <TouchableOpacity style={[chatStyles.message, message.is_my_message === true ? chatStyles.myMessage : null]} onPress={(event) => 
                                {setMenuPos({x:event.nativeEvent.pageX-(message.is_my_message ? 150 : 0), y:event.nativeEvent.pageY-100});
                                setSelected(message);}}>

                                {mediaMessage}
                                {message.text ? <Text style={[globalStyles.text]}>{message.text}</Text> : null}
                            </TouchableOpacity>
                        </View>
                    )
                })}
            </ScrollView>
            </>
        );
    }catch{}
}