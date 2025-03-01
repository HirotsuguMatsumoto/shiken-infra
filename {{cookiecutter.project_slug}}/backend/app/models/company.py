from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from app.db import Base
from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime


class Company(Base):
    __tablename__ = "companys"

    id: Mapped[int] = mapped_column(primary_key=True)

    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    
    name: Mapped[str] = mapped_column(String(200))
