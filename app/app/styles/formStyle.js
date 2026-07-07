import {StyleSheet, useColorScheme} from "react-native";

export function useFormStyle(){
    const color = useColorScheme() === "dark" ? "white" : "black";

    return StyleSheet.create({
        input:{
            alignSelf:"center",
            width:"90%",
            borderColor:color,
            borderBottomWidth:1,
            color:color,
            marginBottom:10
        },
        block:{
            alignItems:"center",
            marginTop:"50%",
            padding:10
        },
        secondaryButton:{
            marginTop:10,
            marginBottom:2
        },
        secondaryText:{
            color:"gray"
        },
        formText:{
            fontSize:25
        },
        button:{
            width:"90%",
            marginTop:10,
            marginBottom:5,
            fontSize:20,
            height:35
        }
    });
}