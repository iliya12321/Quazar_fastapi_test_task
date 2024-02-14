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

    async def top_five_longest_usernames(self) -> list:
        longest_usernames = await self.session.execute(
            select(User.username).order_by(func.length(User.username).desc()).limit(5)
        )
        return longest_usernames.scalars().all()

    async def email_domain_share(self, domain: str):
        total_users = await self.session.execute(select(func.count(User.id)))
        percent_domain = await self.session.execute(
            select(func.count(User.email)).where(User.email.like(f"%@{domain}"))
        )
        try:
            return round((percent_domain.scalar() / total_users.scalar()) * 100, 0)
        except ZeroDivisionError:
            return 0
