from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum as SQLEnum
from src.core.enums import AdminType
from src.core.base.models import Base


class AdminModel(Base):
    __tablename__ = 'admins'
    
    username: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    admin_type: Mapped[AdminType] = mapped_column(SQLEnum(AdminType), nullable=False, default=AdminType.DEFAULTADMIN)
