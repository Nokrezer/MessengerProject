import { websocketUrl } from "@/src/settings/config";
import { authService } from "./authService";

class RealTimeService{
    public websocket;
    constructor(){
        this.websocket = new WebSocket(websocketUrl);
    }

    async sendRegistration(){
        const accessToken = await authService.getAccessToken();
        const request = {ACCESS_TOKEN:accessToken};
        await this.websocket.send(JSON.stringify(request));
    }
}

export const realTimeService = new RealTimeService();