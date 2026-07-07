from settings.config import *

from fastapi import WebSocket

class RouteData():
    def __init__(self, path, func, method):
        self.path = path
        self.func = func
        self.method = method

class Routes():
    def __init__(self, api_controller, auth_controller, server, realtime_core):
        self.api_controller = api_controller
        self.auth_controller = auth_controller
        self.server = server
        self.realtime_core = realtime_core
        
        self.ROUTES = [
                        #АВТОРИЗАЦИЯ и работа с токенами
                        RouteData(AUTH_PREFIX + "login", self.auth_controller.login, ["POST"]),
                        RouteData(AUTH_PREFIX + "registration", self.auth_controller.registration, ["POST"]),
                        RouteData(AUTH_PREFIX + "updateAccessToken", self.auth_controller.update_access_token, ["POST"]),
                        RouteData(AUTH_PREFIX + "verifyRefreshToken", self.auth_controller.verify_refresh_token, ["POST"]),
                        RouteData(AUTH_PREFIX + "verifyAccessToken", self.auth_controller.verify_access_token, ["POST"]),
                        RouteData(AUTH_PREFIX + "loginWithCode", self.auth_controller.login_with_code, ["POST"]),
                        RouteData(AUTH_PREFIX + "requestAuthCode", self.auth_controller.request_auth_code, ["POST"]),
                        RouteData(AUTH_PREFIX + "requestRegCode", self.auth_controller.request_reg_code, ["POST"]),
                        RouteData(AUTH_PREFIX + "getTempToken", self.auth_controller.get_temp_token, ["POST"]),

                        #API
                        RouteData(API_PREFIX + "sendMessage", self.api_controller.send_message, ["POST"]),
                        RouteData(API_PREFIX + "getIdByToken", self.api_controller.get_id_by_token, ["GET"]),
                        RouteData(API_PREFIX + "sendMessage", self.api_controller.send_message, ["POST"]),
                        RouteData(API_PREFIX + "getChats", self.api_controller.get_user_chats, ["GET"]),
                        RouteData(API_PREFIX + "sendPublicKeys", self.api_controller.save_public_keys, ["POST"]),
                        RouteData(API_PREFIX + "getPublicKeys", self.api_controller.get_public_keys, ["GET"]),
                        RouteData(API_PREFIX + "getUsers", self.api_controller.get_users, ["GET"]),
                        RouteData(API_PREFIX + "getMessages", self.api_controller.get_messages, ["GET"]),
                        RouteData(API_PREFIX + "getChatData", self.api_controller.get_chat_data, ["GET"]),
                        RouteData(API_PREFIX + "getChatType", self.api_controller.get_chat_type, ["GET"]),
                        RouteData(API_PREFIX + "getChatMembers", self.api_controller.get_chat_members, ["GET"]),
                        RouteData(API_PREFIX + "createPrivateChat", self.api_controller.create_private_chat, ["POST"]),
                        RouteData(API_PREFIX + "getChatIdByMembers", self.api_controller.get_chat_by_members, ["GET"]),
                        RouteData(API_PREFIX + "getPrivateData", self.api_controller.get_private_data, ["GET"]),
                        RouteData(API_PREFIX + "setUserImage", self.api_controller.set_user_image, ["POST"]),
                        RouteData(API_PREFIX + "getUserImage", self.api_controller.get_user_image, ["GET"]),
                        RouteData(API_PREFIX + "setUserName", self.api_controller.set_user_name, ["POST"]),
                        RouteData(API_PREFIX + "setUserNickname", self.api_controller.set_user_nickname, ["POST"]),
                        RouteData(API_PREFIX + "setUserBio", self.api_controller.set_user_bio, ["POST"]),
                        RouteData(API_PREFIX + "getUserData", self.api_controller.get_user_data, ["GET"]),
                        RouteData(API_PREFIX + "getChatImage", self.api_controller.get_chat_image, ["GET"]),
                        RouteData(API_PREFIX + "getMediaMessage", self.api_controller.get_media_message, ["GET"])
        ]

    def register(self):
        for route in self.ROUTES:
            self.server.add_api_route(route.path, route.func,
                                      methods=route.method)
        
        #для вебсокетов создаём только один путь
        self.server.add_api_websocket_route("/ws", self.realtime_core.register_user)