import { userService } from "../services/fetchServices/userService";
import { authService } from "../services/fetchServices/authService";
import { userApi } from "@/src/settings/config";

export const searchUsersHandler = async (text:string) => {
    const users = await userService.getUsers(text);
    const tempToken = await authService.getTempToken();
    
    for(const user of users){
        user.imageUrl = userApi.getUserImage + "userId=" + user.user_id + "&tempToken=" + tempToken;
    }

    return users;
};