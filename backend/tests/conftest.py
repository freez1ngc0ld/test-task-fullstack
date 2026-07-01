import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.core.base.models import Base
from src.features.admin.service import AdminAuthService
from src.features.application.service import ApplicationService
from src.core.enums import AdminType
from src.core.config import settings


@pytest.fixture
async def db_session():
    engine = create_async_engine(settings.TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session
    await engine.dispose()

@pytest.fixture
def admin_service(db_session):
    return AdminAuthService(db_session)

@pytest.fixture
async def app_service(db_session):
    return ApplicationService(db_session)

@pytest.fixture
async def superadmin(admin_service: AdminAuthService):
    await admin_service.setup_superadmin()
    return await admin_service.admin_repo.get_by_username(settings.ADMIN_USERNAME)

@pytest.fixture
async def defaultadmin(admin_service: AdminAuthService, superadmin):
    default_admin = await admin_service.create_admin(superadmin, "test_user", "password123", AdminType.DEFAULTADMIN)
    return await admin_service.admin_repo.get_by_username(default_admin.username)
