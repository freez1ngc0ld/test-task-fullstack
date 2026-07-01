from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, CheckConstraint, Enum as SQLEnum
from src.core.enums import StatusType, PriorityType
from src.core.base.models import Base


class ApplicationModel(Base):
    __tablename__ = 'applications'
    
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    status: Mapped[StatusType] = mapped_column(SQLEnum(StatusType), nullable=False, default=StatusType.NEW)
    priority: Mapped[PriorityType] = mapped_column(SQLEnum(PriorityType), nullable=False, default=PriorityType.LOW)

    __table_args__ = (
        CheckConstraint('length(title) >= 3', name='title_min_length_check'),
    )
