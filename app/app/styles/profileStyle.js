import {StyleSheet} from "react-native";
import { useNowColor } from "./globalStyles";

export function useProfileStyle(){
    const color = useNowColor();

    return StyleSheet.create({
    userImage:{
        height:250,
        width:250,
        borderRadius:250,
        marginBottom:40,
        marginTop:30,
        alignSelf:"center"
    },
    button:{
        width:"93%",
        height:40
    },
    secondaryText:{
        color:"gray",
        fontSize:11,
        marginLeft:5
    },
    block:{
        marginBottom:10
    }
});
}