// import * as SecureStore from 'expo-secure-store';
// import { Platform } from "react-native";

// export class KeyStorageService{
//     private readonly sessionsListKey;
//     private readonly userId;

//     constructor(userId:string){
//         this.sessionsListKey = `user${userId}SessionsKey`;
//         this.userId = userId;
//     }

//     private async appendSessionsList(sessionId:string){
//     if(Platform.OS == "web"){}
//     else{
//       const rawSessionsList = await SecureStore.getItemAsync(`sessionsList_${this.userId}`);

//       if(!rawSessionsList){//Если ещё не было сессий, добавляем первую
//         await SecureStore.setItemAsync("sessionsList", JSON.stringify([sessionId]));
//         return;
//       }

//       const sessionsList = JSON.parse(rawSessionsList);//Парсим список сессий
//       await SecureStore.setItemAsync("sessionsList", JSON.stringify([...sessionsList, sessionId]));//Добавляем
//     }
//   }

//   async savePrivateKey(privateKey: string) {
//     if(Platform.OS === "web"){
//     }else
//         await SecureStore.setItemAsync(`privateKey_${this.userId}`, privateKey);
//   }

//   async getIdentity(){
//     const privateKey = await SecureStore.getItemAsync(`privateKey_${this.userId}`);
//     return privateKey;
//     // const identity = rawIdentity ? JSON.parse(rawIdentity) : null;
//     // return identity;
//   }

//   async deleteIdentity() {
//     await SecureStore.setItemAsync(`privateKey_${this.userId}`, '');
//   }

// }
