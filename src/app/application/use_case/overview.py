from app.application.dto import OverviewDTO
from app.application.services import AssetTrackerService


class GetAccountOverviewUseCase:
    def __init__(self, service: AssetTrackerService):
        self.service = service
    
    async def execute(self) -> OverviewDTO:
        return await self.service.get_overview()
