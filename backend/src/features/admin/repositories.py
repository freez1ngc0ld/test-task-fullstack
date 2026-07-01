from .models import AdminModel
from src.core.enums import AdminType
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete


class AdminRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, username: str, hashed_password: str, admin_type: AdminType = AdminType.DEFAULTADMIN) -> AdminModel:
        new_admin = AdminModel(username=username, hashed_password=hashed_password, admin_type=admin_type)
        self.db.add(new_admin)
        await self.db.flush()
        return new_admin
    
    async def get_all(self, offset: int | None, limit: int | None) -> list[AdminModel]:
        stmt = select(AdminModel)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        stmt.order_by(AdminModel.created_at.desc())
        admins = (await self.db.execute(stmt)).scalars()
        return admins

    async def get_by_id(self, id: str) -> AdminModel | None:
        stmt = (
            select(AdminModel)
            .where(AdminModel.id == id)
        )
        admin = (await self.db.execute(stmt)).scalar_one_or_none()
        return admin

    async def get_by_username(self, username: str) -> AdminModel | None:
        stmt = (
            select(AdminModel)
            .where(AdminModel.username == username)
        )
        admin = (await self.db.execute(stmt)).scalar_one_or_none()
        return admin
    
    async def delete(self, id: str) -> None:
        await self.db.execute(delete(AdminModel).where(AdminModel.id == id))
        await self.db.flush()

