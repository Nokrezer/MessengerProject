export const siteIp = "http://192.168.31.168:8000/";
const prefixApi = siteIp + "api/";
const prefixAuth = siteIp + "auth/";

export const userApi = {
    getIdByToken: prefixApi + "getIdByToken",
    getChats: prefixApi + "getChats"
};
export const authApi = {
    login: prefixAuth + "login",
    updateAccessToken: prefixAuth + "updateAccessToken",
    verifyAccessToken: prefixAuth + "verifyAccessToken",
    verifyRefreshToken: prefixAuth + "verifyRefreshToken"
};
