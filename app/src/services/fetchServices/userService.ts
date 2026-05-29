import { userApi } from "@/src/settings/config";

class UserService{
    async getIdByToken(accessToken: string){
        const response = await fetch(userApi.getIdByToken, {
            method: "GET",
            headers:{"Authorization":accessToken}
        });

        return await response.json();
    }
}

export const userService = new UserService();