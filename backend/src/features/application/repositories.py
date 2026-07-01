from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, asc, desc,or_, case, Case
from src.core.enums import StatusType, PriorityType
from .models import ApplicationModel

PRIORITY_WEIGHTS = {
    PriorityType.HIGH: 3,
    PriorityType.NORMAL: 2,
    PriorityType.LOW: 1
}


class ApplicationRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    @staticmethod
    def get_priority_order_clause() -> Case[Any]:
        whens = [(ApplicationModel.priority == key, weight) for key, weight in PRIORITY_WEIGHTS.items()]
        return case(*whens, else_=0)

    async def create(self, title: str, description: str | None, status: StatusType, priority: PriorityType) -> ApplicationModel:
        new_application = ApplicationModel(title=title, description=description, status=status, priority=priority)
        self.db.add(new_application)
        await self.db.flush()
        return new_application
    
    async def get_all(
        self, 
        query: str | None = None,
        statuses: list[StatusType] | None = None,
        priorities: list[StatusType] | None = None,
        sort_by_priority: bool = False,
        sort_desc: bool = True,
        offset: int | None = None, 
        limit: int | None = None,
    ) -> list[ApplicationModel]:
        
        stmt = select(ApplicationModel)

        if query:
            search_filter = or_(
                ApplicationModel.title.ilike(f"%{query}%"),
                ApplicationModel.description.ilike(f"%{query}%")
            )
            stmt = stmt.where(search_filter)

        if statuses:
            stmt = stmt.where(ApplicationModel.status.in_(statuses))
        if priorities:
            stmt = stmt.where(ApplicationModel.priority.in_(priorities))

        order_func = desc if sort_desc else asc
        ordering = []

        if sort_by_priority:
            ordering.append(order_func(self.get_priority_order_clause()))
            ordering.append(desc(ApplicationModel.created_at))
        else:
            ordering.append(order_func(ApplicationModel.created_at))

        stmt = stmt.order_by(*ordering)

        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        applications = (await self.db.execute(stmt)).scalars()
        return applications
    
    async def get(self, id: str) -> ApplicationModel | None:
        stmt = (
            select(ApplicationModel)
            .where(ApplicationModel.id == id)
        )
        application = (await self.db.execute(stmt)).scalar_one_or_none()
        return application
    
    async def delete(self, id: str) -> None:
        await self.db.execute(delete(ApplicationModel).where(ApplicationModel.id == id))
        await self.db.flush()

    async def delete_many(self, ids: list[str]) -> int:
        stmt = delete(ApplicationModel).where(
            ApplicationModel.id.in_(ids), 
            ApplicationModel.status != StatusType.DONE
        )
        result = await self.db.execute(stmt)
        count = result.rowcount
        return count
