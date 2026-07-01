from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db.session import get_db
from .service import AdminAuthService


def get_admin_auth_service(db: AsyncSession = Depends(get_db)):
    return AdminAuthService(db)
