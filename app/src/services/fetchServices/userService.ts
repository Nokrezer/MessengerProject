import { authApi, userApi } from "@/src/settings/config";
import { authService } from "./authService";
import { fetchService, FetchService } from "./fetchService";

class UserService{
    private fetchService : FetchService;
    constructor(fetchService:FetchService){
        this.fetchService = fetchService;
    }
    
    async getIdByToken(accessToken: string){
        const response = await this.fetchService.fetch({
            request:userApi.getIdByToken,
            method: "GET",
            headers:{"Authorization":accessToken}
        });

        return response;
    }

    async getUsers(nickname:string){
        const response = await this.fetchService.fetch({
            request:userApi.getUsers + "nickname=" + nickname,
            headers:{
                Authorization: await authService.getAccessToken()
            }
        });

        return response;
    }

    async getPrivateData(){
        const response = await this.fetchService.fetch({
            request:userApi.getPrivateData, 
            headers:{
                Authorization: await authService.getAccessToken()
            }
        });

        return response;
    }

    async getUserImage(userId:string){
        const response = await this.fetchService.fetch({
            request:userApi.getUserImage + "userId=" + userId,
            headers:{
                Authorization: await authService.getTempToken()
            }
        });

        return response;
    }

    async setUserImage(dir:string){
        const form = new FormData();
        form.append("file", {
                    uri: dir,
                    type: 'image/jpeg',
                    name: "image",
                } as any);
        
        await this.fetchService.fetch({
            request:userApi.setUserImage,
            method:"POST",
            headers:{
                Authorization: await authService.getAccessToken()
            },
            body: form
        });
    }

    async setUserName(name:string){
        const form = new FormData();
        form.append("name", name);
        
        await this.fetchService.fetch({
            request:userApi.setUserName,
            method:"POST",
            headers:{
                Authorization: await authService.getAccessToken()
            },
            body: form
        });
    }

    async setUserNickname(nickname:string){
        const form = new FormData();
        form.append("nickname", nickname);
        
        await this.fetchService.fetch({
            request:userApi.setUserNickname,
            method:"POST",
            headers:{
                Authorization: await authService.getAccessToken()
            },
            body: form
        });
    }

    async setUserBio(bio:string){
        const form = new FormData();
        form.append("bio", bio);
        
        await this.fetchService.fetch({
            request:userApi.setUserBio,
            method:"POST",
            headers:{
                Authorization: await authService.getAccessToken()
            },
            body: form
        });
    }
}

export const userService = new UserService(fetchService);