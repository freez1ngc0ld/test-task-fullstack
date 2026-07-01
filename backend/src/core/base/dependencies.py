from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db.session import get_db
from src.core.security.token_manager import TokenManager
from src.core.config import settings
from src.features.admin.models import AdminModel
from src.features.admin.repositories import AdminRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='admin/signin')
token_manager = TokenManager(secret_key=settings.SECRET_KEY)


async def get_current_admin(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> AdminModel:
    admin_id = token_manager.verify_token(token)
    admin_repo = AdminRepository(db)
    admin = await admin_repo.get_by_id(id=admin_id)
    if not admin:
        raise PermissionError()
    return admin