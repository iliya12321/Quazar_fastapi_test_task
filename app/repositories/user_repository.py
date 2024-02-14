import datetime

from sqlalchemy import select, func

from app.db.models import User
from app.repositories.base_repository import Repository


class UserRepository(Repository):
    model = User

    async def count_users_registered_last_seven_days(self):
        count = await self.session.execute(
            select(func.count(User.id)).where(
                User.registration_date
                >= (datetime.datetime.now() - datetime.timedelta(days=7))
            )
        )
        return count.scalar()
