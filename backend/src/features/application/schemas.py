from src.core.base.schemas import BaseSchema
from pydantic import Field
from src.core.enums import StatusType, PriorityType
from datetime import datetime
from typing import Optional

class ApplicationCreateSchema(BaseSchema):
    title: str = Field(min_length=3, max_length=120)
    description: str | None
    status: StatusType
    priority: PriorityType

class ApplicationSchema(ApplicationCreateSchema):
    id: str
    created_at: datetime
    updated_at: datetime

class ApplicationUpdateSchema(BaseSchema):
    title: Optional[str] = Field(default=None, min_length=3, max_length=120)
    description: Optional[str] = None
    status: Optional[StatusType] = None
    priority: Optional[PriorityType] = None

class ApplicationDeleteManySchema(BaseSchema):
    ids: list[str]
