import datetime

from sqlalchemy import BigInteger, DateTime, func, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants.field_limits import FIELD_LIMITS
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(
        String(FIELD_LIMITS["username_max_length"]),
        nullable=False,
        unique=True,
    )
    email: Mapped[str] = mapped_column(
        String(FIELD_LIMITS["email_max_length"]),
        nullable=False,
        unique=True,
    )
    registration_date: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
