from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from .exceptions import *


def register_admin_auth_exception_handlers(app: FastAPI):
    @app.exception_handler(AdminAlreadyExistsException)
    async def admin_already_exists_handler(request: Request, exc: AdminAlreadyExistsException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Админ с таким юзернеймом уже существует"}
        )
    @app.exception_handler(AdminNotFoundException)
    async def admin_not_found_handler(request: Request, exc: AdminNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Админ с таким юзернеймом не найден"}
        )
    @app.exception_handler(InvalidPasswordException)
    async def invalid_password_handler(request: Request, exc: InvalidPasswordException):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Неправильный пароль"}
        )
    @app.exception_handler(PermissionException)
    async def permission_handler(request: Request, exc: PermissionException):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "У вас нет прав для данного действия"}
        )
    @app.exception_handler(AdminDeletionException)
    async def admin_deletional_handler(request: Request, exc: AdminDeletionException):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Главный админ не может удалить сам себя"}
        )
    @app.exception_handler(InvalidTokenException)
    async def invalid_token_handler(request: Request, exc: InvalidTokenException):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Недопустимый токен"}
        )
    @app.exception_handler(TokenExpireException)
    async def token_expire_handler(request: Request, exc: TokenExpireException):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Срок действия токена истёк"}
        )
    