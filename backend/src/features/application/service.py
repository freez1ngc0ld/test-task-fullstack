from sqlalchemy.ext.asyncio import AsyncSession
from src.core.enums import StatusType, PriorityType
from src.core.base.schemas import StatusSchema
from src.core.logger import logger
from .repositories import ApplicationRepository
from .schemas import ApplicationSchema
from .exceptions import (
    ApplicationNotFoundException,
    CantTouchDoneApplicationException,
    CantSetStatusLess
)


statuses = {
    StatusType.NEW: 1,
    StatusType.IN_PROGRESS: 2,
    StatusType.DONE: 3
}


class ApplicationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.application_repo = ApplicationRepository(self.db)

    async def create_application(self, title: str, description: str | None, status: StatusType, priority: PriorityType) -> ApplicationSchema:
        new_application = await self.application_repo.create(title=title, description=description, status=status, priority=priority)
        await self.db.commit()
        logger.info(f'Создана заявка ID: {new_application.id} Title: {new_application.title}')
        return ApplicationSchema.model_validate(new_application)
    
    async def get_all(self, 
            query: str | None, 
            statuses: list[StatusType] | None,
            priorities: list[StatusType] | None,
            sort_by_priority: bool,
            sort_desc: bool,
            offset: int | None, 
            limit: int | None,
    ) -> list[ApplicationSchema]:
        applications = await self.application_repo.get_all(
            query=query,
            statuses=statuses,
            priorities=priorities,
            sort_by_priority=sort_by_priority,
            sort_desc=sort_desc,
            offset=offset,
            limit=limit
        )
        return [ApplicationSchema.model_validate(application) for application in applications]
    
    async def get(self, application_id: str) -> ApplicationSchema:
        application = await self.application_repo.get(id=application_id)
        if not application:
            raise ApplicationNotFoundException()
        return ApplicationSchema.model_validate(application)
    
    async def update_application(
            self, 
            application_id: str, 
            title: str | None = None, 
            description: str | None = None, 
            status: StatusType | None = None, 
            priority: PriorityType | None = None
    ) -> ApplicationSchema:
        application = await self.application_repo.get(id=application_id)
        if not application:
            raise ApplicationNotFoundException()
        if application.status == StatusType.DONE:
            raise CantTouchDoneApplicationException()
        if title is not None:
            application.title = title
        if description is not None:
            application.description = description
        if status is not None:
            if statuses[application.status] > statuses[status]:
                raise CantSetStatusLess()
            application.status = status
        if priority is not None:
            application.priority = priority
        await self.db.commit()
        await self.db.refresh(application)
        logger.info(f'Обновлена заявка ID: {application.id} Title: {application.title}')
        return ApplicationSchema.model_validate(application)
    
    async def delete_applications(self, ids: list[str]) -> StatusSchema:
        count = await self.application_repo.delete_many(ids=ids)
        await self.db.commit()
        logger.info(f'Удалены {count} заявки IDs: {', '.join(ids)}')
        return StatusSchema(status=f'Удалено {count} заявок!')

