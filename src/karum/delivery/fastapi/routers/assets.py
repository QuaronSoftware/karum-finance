from fastapi import APIRouter, Depends
from karum.application.use_case import GetAccountOverviewUseCase
from karum.delivery.fastapi.dependencies import get_account_overview_use_case


assets_router = APIRouter(prefix='/assets')


@assets_router.get('/overview')
async def overview(
    overview_uc: GetAccountOverviewUseCase = Depends(get_account_overview_use_case)
):
    return await overview_uc.execute()

