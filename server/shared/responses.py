from fastapi.responses import HTMLResponse


class SuccessResponse():
    def __new__(self):
        return HTMLResponse(content="success", status_code=200)