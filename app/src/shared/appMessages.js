import Toast from "react-native-toast-message";

export const showError = (error) => {
  Toast.show({
    type: 'error',
    text1: error.message,
    text2: error.cause.detail
  });
};

export const showMessage = (name, text) => {
    Toast.show({
        type: "info",
        text1: name,
        text2: text
    })
};