import uvicorn

# from fastapi.responses import HTMLResponse

#Конфигурация
from settings.config import *

#Главное ядро сервера
from starter.core import Core

import asyncio

class RunServer():
    def __init__(self, core):
        self.core = core
    
    def run_uvicorn(self):
        if USE_CERTS:
            uvicorn.run(self.core.server, host=SERVER_IP, port=SERVER_PORT,
                        ssl_keyfile=CERT_KEY, ssl_certfile=CERT)
        else:
            uvicorn.run(self.core.server, host=SERVER_IP, port=SERVER_PORT)

def main():
    core = Core()

    run_server = RunServer(core)
    run_server.run_uvicorn()


if __name__ == "__main__":
    main()