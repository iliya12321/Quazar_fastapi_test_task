import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.constants.field_limits import FIELD_LIMITS


class UserCreate(BaseModel):
    username: str = Field(min_length=FIELD_LIMITS["username_min_length"])
    email: EmailStr


class UserFromDB(UserCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    registration_date: datetime.datetime
