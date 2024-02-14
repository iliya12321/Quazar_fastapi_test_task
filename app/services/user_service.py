from fastapi import HTTPException, status
from app.api.schemas.users import UserCreate, UserFromDB
from app.utils.unitofwork import IUnitOfWork


class UserService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_user(self, user: UserCreate) -> UserFromDB:
        user_dict: dict = user.model_dump()
        async with self.uow:
            user_from_db = await self.uow.user.add_one(user_dict)
            user_to_return = UserFromDB.model_validate(user_from_db)
            await self.uow.commit()
            return user_to_return

    async def get_user(self, user_id: int) -> UserFromDB | None:
        if user_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User id should be greater than 0",
            )
        async with self.uow:
            user: UserFromDB = await self.uow.user.find_by_id(user_id)
            if user is None:
                raise HTTPException(
                    status_code=404, detail=f"User with id {user_id} not found"
                )
            return UserFromDB.model_validate(user)
