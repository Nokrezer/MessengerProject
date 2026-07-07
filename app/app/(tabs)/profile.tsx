import {SafeAreaView} from 'react-native-safe-area-context';
import {StyleSheet, useColorScheme, TextInput, Text, View, TouchableOpacity} from 'react-native';
import { Image } from 'expo-image';
import {useState, useEffect} from "react";

//стили
import { useGlobalStyles, useNowColor } from '../styles/globalStyles';
import {useProfileStyle} from "@/app/styles/profileStyle";
//хуки
import {useGetUserData} from "@/src/hooks/userDataHook";
//config
import { userApi } from '@/src/settings/config';
//хендлеры
import { onSaveButtonHandler, onEditImageHandler } from '@/src/useCase/profileUseCases';

export default function ProfilePage() {
  const globalStyles = useGlobalStyles();
  const profileStyle = useProfileStyle();

  const {data, imgUrl, loading} = useGetUserData();

  const [name, setName] = useState("");
  const [nickname, setNickname] = useState("");
  const [buttonState, setButtonState] = useState(false);
  const [imageUrl, setImageUrl] = useState("");
  const [bio, setBio] = useState("");

  useEffect(() => {
    if(data){
      setName(data.name);
      setNickname(data.nickname || "");
      setImageUrl(imgUrl);
      setBio(data.bio);
    }
  }, [data]);
  
  if(loading)
    return <Text>Загрузка</Text>;
  
  return (
    <SafeAreaView>
      <TouchableOpacity onPress={async () => setImageUrl(await onEditImageHandler() || imageUrl as string)}>
        <Image source={{uri:imageUrl}} style={profileStyle.userImage}></Image>
      </TouchableOpacity>
      
      <View style={[globalStyles.block, profileStyle.block]}>
        <TextInput style={[globalStyles.text]} onChangeText={(text) => {setName(text); setButtonState(false)}}>
          {data ? data.name : ""}
        </TextInput>

        <Text style={profileStyle.secondaryText}>Имя пользователя</Text>
      </View>

      <View style={[globalStyles.block, profileStyle.block]}>
        <TextInput style={globalStyles.text} value={"@" + (nickname.slice(0,1) === "@" ? nickname.slice(1) : nickname)} 
        onChangeText={(text) => {setNickname(text); setButtonState(false)}}></TextInput>

        <Text style={[profileStyle.secondaryText]}>Ник пользователя</Text>
      </View>

      <View style={[globalStyles.block, profileStyle.block]}>
        <TextInput style={globalStyles.text} value={bio} 
        onChangeText={(text) => {setBio(text); setButtonState(false)}}></TextInput>

        <Text style={[profileStyle.secondaryText]}>Описание профиля</Text>
      </View>

      <TouchableOpacity style={[globalStyles.button, profileStyle.button]} disabled={buttonState} onPress={() => {onSaveButtonHandler(data, name, nickname, bio); setButtonState(true)}}>
        <Text style={globalStyles.text}>Сохранить</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
}