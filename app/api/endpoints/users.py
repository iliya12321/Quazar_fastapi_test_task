from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.exc import IntegrityError

from app.api.schemas.users import (
    UserCreate,
    UserFromDB,
)
from app.core.constants.integer_constants import INTEGER_CONSTANTS
from app.services.user_service import UserService
from app.utils.unitofwork import IUnitOfWork, UnitOfWork

users_router = APIRouter(prefix="/users", tags=["users"])


async def get_user_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> UserService:
    return UserService(uow)


@users_router.get(
    "",
    response_model=list[UserFromDB],
    status_code=status.HTTP_200_OK,
)
async def get_users(
    page: int = Query(
        default=INTEGER_CONSTANTS["page_default"],
        description="Номер страницы",
        gt=0,
    ),
    size: int = Query(
        default=INTEGER_CONSTANTS["size_default"],
        description="Размер страницы",
        gt=0,
    ),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_users(page, size)


@users_router.get(
    "/{user_id}",
    response_model=UserFromDB,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_user(user_id)
    return user


@users_router.post(
    "",
    response_model=UserFromDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    try:
        return await user_service.add_user(user)
    except IntegrityError as e:
        if "email" in e.orig.args[0]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{user.email} already exists",
            )
        elif "username" in e.orig.args[0]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{user.username} already exists",
            )
