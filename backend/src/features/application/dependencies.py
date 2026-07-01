from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db.session import get_db
from .service import ApplicationService


def get_application_service(db: AsyncSession = Depends(get_db)) -> ApplicationService:
    return ApplicationService(db)