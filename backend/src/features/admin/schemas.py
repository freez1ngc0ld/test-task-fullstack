from src.core.base.schemas import BaseSchema
from src.core.enums import AdminType
from datetime import datetime


class AdminAccountDeleteSchema(BaseSchema):
    admin_2_delete_id: str


class DeleteMyAccountSchema(BaseSchema):
    password: str


class AdminChangePasswordSchema(BaseSchema):
    old_password: str
    new_password: str


class AdminCreateSchema(BaseSchema):
    username: str
    password: str


class AdminSchema(BaseSchema):
    id: str
    username: str
    admin_type: AdminType
    created_at: datetime
    updated_at: datetime

class AccessTokenSchema(BaseSchema):
    access_token: str
    token_type: str = "Bearer"
