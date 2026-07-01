import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from src.core.base.models import Base
from src.core.db.session import engine, AsyncSessionLocal
from src.core.config import settings
from src.core.logger import setup_logger
from src.features.admin.service import AdminAuthService
from src.features.admin.router import admin_auth_router
from src.features.application.router import application_router
from src.features.admin.handlers import register_admin_auth_exception_handlers
from src.features.application.handlers import register_application_exception_handlers


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as db:
        await AdminAuthService(db=db).setup_superadmin()
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan, title=settings.APP_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)

app.include_router(router=admin_auth_router)
app.include_router(router=application_router)

register_admin_auth_exception_handlers(app=app)
register_application_exception_handlers(app=app)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "detail": "Ошибка валидации",
            "errors": exc.errors() 
        }
    )

setup_logger()

if __name__ == '__main__':
    uvicorn.run(app='src.main:app', host=settings.HOST, port=settings.PORT, reload=settings.RELOAD)
