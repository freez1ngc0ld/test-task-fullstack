from fastapi import APIRouter, Depends, Query, status
from typing import Optional
from src.core.base.schemas import StatusSchema
from src.features.admin.models import AdminModel
from src.core.enums import StatusType, PriorityType
from src.core.base.dependencies import get_current_admin
from .service import ApplicationService
from .dependencies import get_application_service
from .schemas import (
    ApplicationSchema, 
    ApplicationCreateSchema,
    ApplicationUpdateSchema,
)


application_router = APIRouter(prefix='/applications', tags=['Application'])


@application_router.post('/', response_model=ApplicationSchema, status_code=status.HTTP_201_CREATED)
async def create_application(
    payload: ApplicationCreateSchema, 
    service: ApplicationService = Depends(get_application_service)
):
    return await service.create_application(
        title=payload.title, 
        description=payload.description, 
        status=payload.status, 
        priority=payload.priority
    )

@application_router.get('/', response_model=list[ApplicationSchema], status_code=status.HTTP_200_OK)
async def get_all_applications(
    query: Optional[str] = None,
    statuses: Optional[list[StatusType]] = Query(None),
    priorities: Optional[list[PriorityType]] = Query(None),
    sort_by_priority: bool = False,
    sort_desc: bool = True,
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: ApplicationService = Depends(get_application_service)
):
    return await service.get_all(
        query=query,
        statuses=statuses,
        priorities=priorities,
        sort_by_priority=sort_by_priority,
        sort_desc=sort_desc,
        offset=offset,
        limit=limit
    )

@application_router.patch('/{application_id}', response_model=ApplicationSchema, status_code=status.HTTP_200_OK)
async def update_application(
    application_id: str,
    payload: ApplicationUpdateSchema,
    service: ApplicationService = Depends(get_application_service)
):
    return await service.update_application(
        application_id=application_id,
        **payload.model_dump(exclude_unset=True)
    )

@application_router.delete('/delete-many', response_model=StatusSchema, status_code=status.HTTP_200_OK)
async def delete_many(
    ids: list[str], 
    admin: AdminModel = Depends(get_current_admin), 
    service: ApplicationService = Depends(get_application_service)
):
    return await service.delete_applications(ids=ids)