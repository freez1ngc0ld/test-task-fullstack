from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from .exceptions import *


def register_application_exception_handlers(app: FastAPI):
    @app.exception_handler(ApplicationNotFoundException)
    async def admin_already_exists_handler(request: Request, exc: ApplicationNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Такой заявки не существует"}
        )
    @app.exception_handler(CantTouchDoneApplicationException)
    async def cant_touch_done_application_handler(request: Request, exc: CantTouchDoneApplicationException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Вы не можете изменять / удалять заявку с статусом DONE"}
        )