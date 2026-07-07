import {StyleSheet} from "react-native";
import { useNowColor } from "./globalStyles";

export function useUserButtonStyle(){
    const color = useNowColor();

    return StyleSheet.create({
    chatButton:{
        height:70,
        flexDirection:"row",
        paddingLeft:15,
        paddingTop:5,
        paddingBottom:5
    },
    image:{
        width:60,
        height:60,
        borderRadius:100
    },
    userName:{
        fontSize:20,
        top:5,
        left:10
    },
    nickname:{
        color:"gray",
        fontSize:12,
        top:5,
        left:15
    }
});
}