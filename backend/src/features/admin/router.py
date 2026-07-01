from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from src.core.base.schemas import StatusSchema
from src.core.base.dependencies import get_current_admin
from .dependencies import get_admin_auth_service
from .models import AdminModel
from .service import AdminAuthService
from .schemas import (
    AdminSchema, 
    AdminAccountDeleteSchema,
    AdminCreateSchema, 
    AdminChangePasswordSchema, 
    AccessTokenSchema,
    DeleteMyAccountSchema
)

admin_auth_router = APIRouter(prefix='/admin', tags=['Admin Auth'])

@admin_auth_router.get('/is_super_admin/{admin_id}', status_code=status.HTTP_200_OK, response_model=dict[str, bool])
async def is_super_admin(
    admin_id: str, 
    admin_auth_service: AdminAuthService = Depends(get_admin_auth_service)
):
    return {'is_super_admin': await admin_auth_service.is_super_admin(admin_id=admin_id)}

@admin_auth_router.get('/me', status_code=status.HTTP_200_OK, response_model=AdminSchema)
def get_me(admin: AdminModel = Depends(get_current_admin), admin_auth_service: AdminAuthService = Depends(get_admin_auth_service)):
    return admin_auth_service.get_me(admin=admin)

@admin_auth_router.get('/all', status_code=status.HTTP_200_OK, response_model=list[AdminSchema])
async def get_all_admins(
    offset: int | None = None, 
    limit: int | None = None, 
    admin: AdminModel = Depends(get_current_admin), 
    admin_auth_service: AdminAuthService = Depends(get_admin_auth_service)
):
    return await admin_auth_service.get_all_admins(admin=admin, offset=offset, limit=limit)

@admin_auth_router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=AdminSchema)
async def create_admin(
    payload: AdminCreateSchema, 
    admin: AdminModel = Depends(get_current_admin), 
    admin_auth_service: AdminAuthService = Depends(get_admin_auth_service)
):
    return await admin_auth_service.create_admin(admin=admin, username=payload.username, password=payload.password)

@admin_auth_router.post('/signin', status_code=status.HTTP_200_OK, response_model=AccessTokenSchema)
async def login_admin(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    admin_auth_service: AdminAuthService = Depends(get_admin_auth_service)
):
    return await admin_auth_service.login_admin(username=form_data.username, password=form_data.password)

@admin_auth_router.patch('/change-password', status_code=status.HTTP_200_OK, response_model=StatusSchema)
async def change_admin_password(
    payload: AdminChangePasswordSchema, 
    admin: AdminModel = Depends(get_current_admin), 
    admin_auth_service: AdminAuthService = Depends(get_admin_auth_service)
):
    return await admin_auth_service.change_password(admin=admin, old_password=payload.old_password, new_password=payload.new_password)

@admin_auth_router.delete('/delete-account', status_code=status.HTTP_200_OK, response_model=StatusSchema)
async def delete_admin_account(
    payload: AdminAccountDeleteSchema, 
    admin: AdminModel = Depends(get_current_admin), 
    admin_auth_service: AdminAuthService = Depends(get_admin_auth_service)
):
    return await admin_auth_service.delete_admin(admin=admin, admin_2_delete_id=payload.admin_2_delete_id)

@admin_auth_router.delete('/delete-account/me', status_code=status.HTTP_200_OK, response_model=StatusSchema)
async def delete_my_account(
    payload: DeleteMyAccountSchema,
    admin: AdminModel = Depends(get_current_admin), 
    admin_auth_service: AdminAuthService = Depends(get_admin_auth_service)
):
    return await admin_auth_service.delete_my_account(admin=admin, password=payload.password)
