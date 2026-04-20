from fastapi import Request, Depends
from karum.application.use_case import (
    CreateUserIfNotExistsUseCase,
    GetAccountOverviewUseCase
)
from karum.application.container import AppContainer


def get_container(request: Request) -> AppContainer:
    return request.app.state.container


def get_create_user_use_case(
    container: AppContainer = Depends(get_container),
) -> CreateUserIfNotExistsUseCase:
    return container.make_create_user_if_not_exists_use_case()

def get_account_overview_use_case(
    container: AppContainer = Depends(get_container),
) -> GetAccountOverviewUseCase:
    return container.make_get_account_overview_use_case()
