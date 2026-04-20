from ..ports import UoWFactory


class UserService:
    def __init__(self, uow: UoWFactory):
        self.uow = uow

    async def create_user_if_not_exists(self, user_id: str, username: str | None, fullname: str):
        async with self.uow as db:
            await db.users.create(user_id=user_id, username=username, fullname=fullname)
        return True