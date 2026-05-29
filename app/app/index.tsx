// import { SafeAreaView, SafeAreaProvider } from 'react-native-safe-area-context';
// import {StyleSheet, useColorScheme, TextInput, Text, View, Button} from 'react-native';
// import {useState} from "react";

// import {useUpdateAccessToken, useUserAuth} from "../hooks/authHook.js";

// // import "react-native-get-random-values";
// // import { getRandomValues } from 'expo-random';
// // import nacl from "tweetnacl";

// // import { hmac } from "noble-hashes/lib/hmac";
// // import { sha256 } from "noble-hashes/lib/sha256";

// // function KDF(key:any, info:any) {
// //   return hmac(sha256, key, info);
// // }

// // class SessionState{
// //   sendedMessages:number;
// //   receivedMessages:number;

// //   constructor(){
// //     this.sendedMessages = 0;
// //     this.receivedMessages = 0;
// //   }
// // }

// export default function HomeScreen() {
//     // const keys_1 = nacl.box.keyPair();
//     // const keys_2 = nacl.box.keyPair();

//     // const session_1 = new SessionState();
//     // const session_2 = new SessionState();

//     // let nonce = nacl.randomBytes(24);

//     // const encoder = new TextEncoder();
//     // const decoder = new TextDecoder();

//     // const sharedKey = nacl.box.before(keys_2.publicKey, keys_1.secretKey);
//     // const sessionKey = KDF(sharedKey, "session");
//     // const messageKey = KDF(sessionKey, "message_" + session_1.sendedMessages);
//     // session_1.sendedMessages++;

//     // const cryptMessage = nacl.secretbox(encoder.encode("test message"), nonce, messageKey);//nacl.box(encoder.encode("test message"), nonce, keys_2.publicKey, keys_1.secretKey);
    
//     // const sharedKey_2 = nacl.box.before(keys_1.publicKey, keys_2.secretKey);
//     // const sessionKey_2 = KDF(sharedKey_2, "session");
//     // const messageKey_2 = KDF(sessionKey_2, "message_" + session_2.receivedMessages);
//     // session_2.receivedMessages++;

//     // const encryptMessage = nacl.secretbox.open(cryptMessage, nonce, messageKey_2);

//     // nonce = nacl.randomBytes(24);
  
//   const colorScheme = useColorScheme();
//   const textColor = colorScheme === "dark" ? "white" : "black";

//   const [loginValue, setLogin] = useState("");
//   const [passwordValue, setPassword] = useState("");
  
//   return (
//     <SafeAreaProvider>
//       <SafeAreaView>
//         <View>
//           <Text style={{color:textColor}}>Вход в аккаунт</Text>
//           <TextInput style={[styles.textInput, {color:textColor}]} onChangeText={setLogin}></TextInput>
//           <TextInput style={[styles.textInput, {color:textColor}]} onChangeText={setPassword}></TextInput>
//           <Button title="send" onPress={async () => await useUserAuth(loginValue, passwordValue)}></Button>
//           <Button title="update access" onPress={async () => await useUpdateAccessToken()}></Button>
//         </View>
//       </SafeAreaView>
//     </SafeAreaProvider>
//   );
// }

// const styles = StyleSheet.create({
//   textInput:{
//     outline: "none",
//     borderColor:"white",
//   },

//   // button:{
//     // color:
//   // }
// });
