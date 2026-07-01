from sqlalchemy.ext.asyncio import AsyncSession
from src.core.enums import AdminType
from src.core.base.schemas import StatusSchema
from src.core.security.token_manager import TokenManager
from src.core.security.password_manager import PasswordManager
from src.core.config import settings
from src.core.logger import logger
from .repositories import AdminRepository
from .models import AdminModel
from .schemas import AdminSchema, AccessTokenSchema
from .exceptions import (
    AdminAlreadyExistsException,
    AdminNotFoundException,
    InvalidPasswordException,
    PermissionException,
    AdminDeletionException
)


class AdminAuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.admin_repo = AdminRepository(self.db)
        self.token_manager = TokenManager(secret_key=settings.SECRET_KEY)
        self.password_manager = PasswordManager()

    async def setup_superadmin(self) -> None:
        admin_exists = await self.admin_repo.get_by_username(username=settings.ADMIN_USERNAME)
        if not admin_exists:
            await self.admin_repo.create(
                username=settings.ADMIN_USERNAME, 
                hashed_password=self.password_manager.hash_password(settings.ADMIN_PASSWORD),
                admin_type=AdminType.SUPERADMIN
            )
            await self.db.commit()
            logger.info(f'Создан суперадмин {settings.ADMIN_USERNAME}')

    async def is_super_admin(self, admin_id: str) -> bool:
        admin = await self.admin_repo.get_by_id(id=admin_id)
        if not admin:
            return False
        return admin.admin_type == AdminType.SUPERADMIN

    def get_me(self, admin: AdminModel) -> AdminSchema:
        return AdminSchema.model_validate(admin)

    async def get_all_admins(self, admin: AdminModel, offset: int | None, limit: int | None) -> list[AdminSchema]:
        if admin.admin_type != AdminType.SUPERADMIN:
            logger.warning(f'Админ {admin.username} попытался получить доступ к эндпоинту get_all_admins, доступному только для суперадмина')
            raise PermissionException()
        admins = await self.admin_repo.get_all(offset=offset, limit=limit)
        return [AdminSchema.model_validate(admin) for admin in admins]

    async def create_admin(self, admin: AdminModel, username: str, password: str, admin_type: AdminType = AdminType.DEFAULTADMIN) -> AdminSchema:
        if admin.admin_type != AdminType.SUPERADMIN:
            logger.warning(f'Админ {admin.username} попытался получить доступ к эндпоинту create_admin, доступному только для суперадмина')
            raise PermissionException()
        hashed_password = self.password_manager.hash_password(password)
        admin_exists = await self.admin_repo.get_by_username(username=username)
        if admin_exists:
            raise AdminAlreadyExistsException()
        admin = await self.admin_repo.create(username=username, hashed_password=hashed_password, admin_type=admin_type)
        await self.db.commit()
        logger.info(f'Был создан админ {admin.username}')
        return AdminSchema.model_validate(admin)
    
    async def login_admin(self, username: str, password: str) -> AccessTokenSchema:
        admin = await self.admin_repo.get_by_username(username=username)
        if not admin:
            raise AdminNotFoundException()
        verify = self.password_manager.verify_password(plain_password=password, hashed_password=admin.hashed_password)
        if not verify:
            raise InvalidPasswordException()
        token = self.token_manager.generate_new_token(sub=admin.id, expires=settings.TOKEN_EXPIRES_SECONDS)
        logger.info(f'Админ {admin.username} был успешно авторизован')
        return AccessTokenSchema(access_token=token)
    
    async def change_password(self, admin: AdminModel, old_password: str, new_password: str) -> StatusSchema:
        new_hashed_password = self.password_manager.hash_password(new_password)
        verify = self.password_manager.verify_password(plain_password=old_password, hashed_password=admin.hashed_password)
        if not verify:
            raise InvalidPasswordException()
        admin.hashed_password = new_hashed_password
        await self.db.commit()
        logger.info(f'Админ {admin.username} успешно изменил пароль')
        return StatusSchema(status='Пароль успешно изменён!')
    
    async def delete_admin(self, admin: AdminModel, admin_2_delete_id: str) -> StatusSchema:
        if admin.admin_type != AdminType.SUPERADMIN:
            logger.warning(f'Админ {admin.username} попытался получить доступ к эндпоинту delete_admin, доступному только для суперадмина')
            raise PermissionException()
        if admin.id == admin_2_delete_id:
            raise AdminDeletionException() 
        admin_2_delete = await self.admin_repo.get_by_id(id=admin_2_delete_id)
        if not admin_2_delete:
            raise AdminNotFoundException()
        await self.admin_repo.delete(admin_2_delete_id)
        await self.db.commit()
        logger.info(f'Суперадмин {admin.username} удалил админа {admin_2_delete.username}')
        return StatusSchema(status=f'Админ {admin_2_delete.username} удалён!')

    async def delete_my_account(self, admin: AdminModel, password: str) -> StatusSchema:
        if admin.admin_type == AdminType.SUPERADMIN:
            raise AdminDeletionException()
        if not self.password_manager.verify_password(password, admin.hashed_password):
            raise InvalidPasswordException()
        await self.admin_repo.delete(admin.id)
        await self.db.commit()
        logger.info(f'Админ {admin.username} удалил свой аккаунт')
        return StatusSchema(status=f'Ваш аккаунт {admin.username} успешно удалён!')
