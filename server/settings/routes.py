from settings.config import *

class RouteData():
    def __init__(self, path, func, method):
        self.path = path
        self.func = func
        self.method = method

class RegisterRoutes():
    def __init__(self, api_controller, auth_controller, server):
        self.api_controller = api_controller
        self.auth_controller = auth_controller
        self.server = server
        
        self.ROUTES = [
                        #АВТОРИЗАЦИЯ
                        RouteData(AUTH_PREFIX + "login", self.auth_controller.login, ["POST"]),
                        RouteData(AUTH_PREFIX + "registration", self.auth_controller.registration, ["POST"]),
                        RouteData(AUTH_PREFIX + "updateAccessToken", self.auth_controller.update_access_token, ["POST"]),
                        RouteData(AUTH_PREFIX + "verifyRefreshToken", self.auth_controller.verify_refresh_token, ["POST"]),
                        RouteData(AUTH_PREFIX + "verifyAccessToken", self.auth_controller.verify_access_token, ["POST"]),

                        #API
                        RouteData(API_PREFIX + "sendMessage", self.api_controller.send_message, ["POST"]),
                        RouteData(API_PREFIX + "getIdByToken", self.api_controller.get_id_by_token, ["GET"]),
                        RouteData(API_PREFIX + "sendMessage", self.api_controller.send_message, ["POST"]),
                        RouteData(API_PREFIX + "getChats", self.api_controller.get_user_chats, ["GET"])
        ]

    def register(self):
        for route in self.ROUTES:
            self.server.add_api_route(route.path, route.func,
                                      methods=route.method)
