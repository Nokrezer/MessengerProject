import {useColorScheme, StyleSheet} from "react-native";

//стандартные стилистики для многих компонентов
export const blockColor = "#101010";
export const borderRadius = 6;

export function useNowColor(){
    const colorScheme = useColorScheme();
    const color = colorScheme === "dark" ? "white" : "black";

    return color;
}

export function useGlobalStyles(){
    const color = useNowColor();
    
    const styles = StyleSheet.create({
        mainView:{
            paddingLeft:2,
            paddingRight:2
        },
        text:{
            color:color
        },
        input:{
            borderWidth:1,
            borderColor:"white",
            borderRadius:borderRadius,
            color:"white"
        },
        centerX:{
            alignSelf:"center"
        },
        button:{
            color:color,
            borderColor:color,
            borderWidth:0.7,
            alignItems:"center",
            justifyContent:"center",
            borderRadius:borderRadius,
            verticalAlign:"middle",
            backgroundColor:blockColor,
            alignSelf:"center"
        },
        rowContainer:{
            flexDirection:'row'
        },
        block:{
            backgroundColor:blockColor,
            width:"93%",
            borderRadius:borderRadius,
            alignSelf:"center"
        }
    });

    return styles;
}

export const globalColors = {
    placeHolder:"gray"
};