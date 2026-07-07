import {useColorScheme, StyleSheet} from "react-native";

export const chatStyles = StyleSheet.create({
    input:{
        flex:1
    },
    button:{
        width:40,
        height:40,
        marginLeft:5
    },
    sendMessageBar:{
        paddingLeft:5,
        paddingRight:5,
        height:40,
        marginBottom:10
    },
    messagesView:{
        height:"91%",
        width:"100%",
        padding:10
    },
    myMessage:{
        textAlign:"right",
        alignSelf:"flex-end"
    },
    message:{
        padding:6,
        backgroundColor:"#7c57eb",
        borderRadius:5,
        alignSelf:"flex-start",
        marginBottom:10
    }
});