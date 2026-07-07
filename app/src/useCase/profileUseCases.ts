import { userService } from "../services/fetchServices/userService";

import * as ImagePicker from 'expo-image-picker';

import { showMessage } from "../shared/appMessages";
import { showError } from "../shared/appMessages";

export async function onSaveButtonHandler(startData:{name:string, nickname:string, bio:string}, name:string, nickname:string, bio:string){
    try{
        if(startData.name !== name){
            await userService.setUserName(name);
            startData.name = name;
        }
        
        if(startData.nickname !== nickname){
            await userService.setUserNickname(nickname.slice(1));
            startData.nickname = nickname;
        }

        if(startData.bio !== bio){
            await userService.setUserBio(bio);
            startData.bio = bio;
        }

        showMessage("Сохранено");
    }catch(error){
        showError(error || "");
    }
}

export async function onEditImageHandler(){
    const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!permission.granted) {
        showError({text:"Нужно разрешение"});
        return;
    }

    const result: ImagePicker.ImagePickerResult = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ['images'],
        allowsEditing: true,
        quality: 1,
    });

    if(!result.assets)
        return;

    const dir = result.assets[0].uri;

    await userService.setUserImage(dir);

    showMessage("Сохранено");

    return dir;
}