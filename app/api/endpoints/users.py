from fastapi import APIRouter, Depends, Query, status, HTTPException
from fastapi.responses import JSONResponse
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
    "/info",
    status_code=status.HTTP_200_OK,
)
async def info(
    user_service: UserService = Depends(get_user_service),
) -> JSONResponse:
    count_users_registered_last_seven_days: int = (
        await user_service.count_users_registered_last_seven_days()
    )
    top_five_longest_usernames: list = await user_service.top_five_longest_usernames()
    return {
        "count_users_registered_last_seven_days": count_users_registered_last_seven_days,
        "top_five_longest_usernames": top_five_longest_usernames,
    }


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


@users_router.put(
    "/{user_id}",
    response_model=UserFromDB,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: int,
    user: UserCreate,
    user_service=Depends(get_user_service),
):
    try:
        return await user_service.update_user(user_id, user)
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


@users_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    await user_service.delete_user(user_id)
