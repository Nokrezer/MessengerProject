import Toast from "react-native-toast-message";

export const showError = ({error, text}:{error?:Error, text?:string}) => {
  Toast.show({
    type: 'error',
    text1:  error?.message || text
  });
};

export const showMessage = (text:string, name?:string) => {
    Toast.show({
        type: "info",
        text1: name || "",
        text2: text
    })
};