from app.application.services import UserService


class CreateUserIfNotExistsUseCase:
    def __init__(self, service: UserService):
        self.service = service
    
    async def execute(self, user_id: str, username: str | None, fullname: str) -> bool:
        return await self.service.create_user_if_not_exists(user_id=user_id, username=username, fullname=fullname)
