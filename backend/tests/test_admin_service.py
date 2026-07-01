import pytest
from src.core.config import settings
from src.features.admin.models import AdminModel
from src.features.admin.service import AdminAuthService
from src.features.admin.exceptions import *
from src.core.enums import AdminType

@pytest.mark.asyncio
async def test_admin_lifecycle(admin_service: AdminAuthService, superadmin: AdminModel):
    new_admin_username = 'admin1'
    new_admin_password = '12345678'
    new_admin = await admin_service.create_admin(admin=superadmin, username=new_admin_username, password=new_admin_password)
    assert new_admin_username == new_admin.username
    new_admin_model = await admin_service.admin_repo.get_by_id(new_admin.id)
    hashed_password = new_admin_model.hashed_password
    assert admin_service.password_manager.verify_password(plain_password=new_admin_password, hashed_password=hashed_password)

    await admin_service.login_admin(username=new_admin_username, password=new_admin_password)

    new_password = '1234567890'
    await admin_service.change_password(admin=new_admin_model, old_password=new_admin_password, new_password=new_password)
    new_admin_model = await admin_service.admin_repo.get_by_id(new_admin.id)
    hashed_password = new_admin_model.hashed_password
    assert admin_service.password_manager.verify_password(plain_password=new_password, hashed_password=hashed_password)

    await admin_service.delete_my_account(admin=new_admin_model, password=new_password)
    new_admin_model = await admin_service.admin_repo.get_by_id(new_admin.id)
    assert new_admin_model is None


@pytest.mark.asyncio
async def test_get_all_admins_permission(admin_service: AdminAuthService, defaultadmin: AdminModel):
    with pytest.raises(PermissionException):
        await admin_service.get_all_admins(defaultadmin, 0, 10)

@pytest.mark.asyncio
async def test_create_admin_permission_and_exists(admin_service: AdminAuthService, defaultadmin: AdminModel):
    with pytest.raises(PermissionException):
        await admin_service.create_admin(defaultadmin, "hacker", "pass")
    
    with pytest.raises(AdminAlreadyExistsException):
        await admin_service.create_admin(await admin_service.admin_repo.get_by_username(settings.ADMIN_USERNAME), "test_user", "pass")

@pytest.mark.asyncio
async def test_login_admin_errors(admin_service: AdminAuthService, superadmin: AdminModel):
    with pytest.raises(AdminNotFoundException):
        await admin_service.login_admin("nobody", "pass")

    with pytest.raises(InvalidPasswordException):
        await admin_service.login_admin(settings.ADMIN_USERNAME, "wrong_pass")

@pytest.mark.asyncio
async def test_change_password_invalid(admin_service: AdminAuthService, defaultadmin: AdminModel):
    with pytest.raises(InvalidPasswordException):
        await admin_service.change_password(defaultadmin, "wrong_old_pass", "new_pass")

@pytest.mark.asyncio
async def test_delete_admin_logic(admin_service: AdminAuthService, superadmin, defaultadmin: AdminModel):
    with pytest.raises(AdminDeletionException):
        await admin_service.delete_my_account(superadmin, settings.ADMIN_PASSWORD)

    with pytest.raises(AdminDeletionException):
        await admin_service.delete_admin(superadmin, superadmin.id)

    with pytest.raises(AdminNotFoundException):
        await admin_service.delete_admin(superadmin, "non-existent-id")

@pytest.mark.asyncio
async def test_delete_my_account_invalid_password(admin_service: AdminAuthService, defaultadmin: AdminModel):
    with pytest.raises(InvalidPasswordException):
        await admin_service.delete_my_account(defaultadmin, "wrong_password")

@pytest.mark.asyncio
async def test_delete_admin_by_superadmin_success(admin_service: AdminAuthService, superadmin: AdminModel):
    target_admin = await admin_service.create_admin(
        admin=superadmin, 
        username="target_user", 
        password="password123", 
        admin_type=AdminType.DEFAULTADMIN
    )

    result = await admin_service.delete_admin(superadmin, target_admin.id)
    assert "удалён" in result.status

    deleted_admin = await admin_service.admin_repo.get_by_id(target_admin.id)
    assert deleted_admin is None

@pytest.mark.asyncio
async def test_delete_admin_by_defaultadmin_fails(admin_service: AdminAuthService, superadmin: AdminModel, defaultadmin: AdminModel):
    victim_admin = await admin_service.create_admin(
        admin=superadmin, 
        username="victim_admin", 
        password="password123", 
        admin_type=AdminType.DEFAULTADMIN
    )
    with pytest.raises(PermissionException):
        await admin_service.delete_admin(defaultadmin, victim_admin.id)
