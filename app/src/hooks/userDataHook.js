import {useState, useEffect} from "react";

import {userService} from "@/src/services/fetchServices/userService";
import { authService } from "../services/fetchServices/authService";

import { userApi } from "../settings/config";

export function useGetUserData(){
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState({name:"", nickname:"", user_id:"", bio:""});
    const [imgUrl, setImageUrl] = useState("");

    useEffect(() => {(async () => {
        const userData = await userService.getPrivateData();
        const tempToken = await authService.getTempToken();
        const url = userApi.getUserImage + `userId=${userData.user_id}` + `&tempToken=${tempToken}`;
        
        setData(userData || {});
        setImageUrl(url);//генерируем ссылку для получения автарки пользователя
        setLoading(false);
    })()}, []);

    return {data, imgUrl, loading};
}