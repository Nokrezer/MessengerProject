const siteIp = "nokrezer.messenger.mooo.com:8000";
export const apiUrl = `https://${siteIp}/`;
export const websocketUrl = `ws://${siteIp}/ws`;
const prefixApi = apiUrl + "api/";
const prefixAuth = apiUrl + "auth/";

export const userApi = {
    getIdByToken: prefixApi + "getIdByToken",
    getChats: prefixApi + "getChats",
    sendMessage: prefixApi + "sendMessage",
    sendPublicKeys: prefixApi + "sendPublicKeys",
    getUsers: prefixApi + "getUsers?",
    getPublicKeys: prefixApi + "getPublicKeys?",
    getMessages: prefixApi + "getMessages?",
    getChatData: prefixApi + "getChatData?",
    getChatType: prefixApi + "getChatType?",
    getChatMembers: prefixApi + "getChatMembers?",
    createPrivateChat: prefixApi + "createPrivateChat?",
    getChatIdByMembers: prefixApi + "getChatIdByMembers?",
    getPrivateData: prefixApi + "getPrivateData",
    getUserImage: prefixApi + "getUserImage?",
    getUserData: prefixApi + "getUserData?",
    setUserImage: prefixApi + "setUserImage",
    setUserName: prefixApi + "setUserName",
    setUserNickname: prefixApi + "setUserNickname",
    setUserBio: prefixApi + "setUserBio",
    getChatImage: prefixApi + "getChatImage?",
    getMediaMessage: prefixApi + "getMediaMessage?"
};
export const authApi = {
    registration: prefixAuth + "registration",
    login: prefixAuth + "login",
    updateAccessToken: prefixAuth + "updateAccessToken",
    verifyAccessToken: prefixAuth + "verifyAccessToken",
    verifyRefreshToken: prefixAuth + "verifyRefreshToken",
    requestAuthCode: prefixAuth + "requestAuthCode",
    requestRegCode: prefixAuth + "requestRegCode",
    loginWithCode: prefixAuth + "loginWithCode",
    getTempToken: prefixAuth + "getTempToken",
};
