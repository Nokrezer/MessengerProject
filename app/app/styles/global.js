import {useColorScheme, StyleSheet} from "react-native";

const colorScheme = useColorScheme();
const textColor = colorScheme === "dark" ? "white" : "black";

export const globalStyles = {
    textColor:{
        color:textColor
    }
};