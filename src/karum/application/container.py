from dataclasses import dataclass

from karum.config import AppSettings
from .ports import (
    UoWFactory,
    WalletProvider,
    PriceProvider,
    CategoryReader
)
from .services import UserService, AssetTrackerService
from .use_case import (
    CreateUserIfNotExistsUseCase,
    GetAccountOverviewUseCase
)


@dataclass(slots=True)
class AppServices:
    users: UserService
    asset_tracker: AssetTrackerService


@dataclass(slots=True)
class AppUseCases:
    create_user: CreateUserIfNotExistsUseCase
    get_overview: GetAccountOverviewUseCase


@dataclass(slots=True)
class AppContainer:
    uow_factory: UoWFactory
    settings: AppSettings
    price_provider: PriceProvider
    category_reader: CategoryReader
    wallet_providers: tuple[WalletProvider, ...]

    def make_user_service(self) -> UserService:
        return UserService(self.uow_factory)

    def make_asset_tracker_service(self) -> AssetTrackerService:
        return AssetTrackerService(
            self.uow_factory,
            self.price_provider,
            self.category_reader,
            self.wallet_providers,
        )

    def make_create_user_if_not_exists_use_case(self) -> CreateUserIfNotExistsUseCase:
        return CreateUserIfNotExistsUseCase(self.make_user_service())

    def make_get_account_overview_use_case(self) -> GetAccountOverviewUseCase:
        return GetAccountOverviewUseCase(self.make_asset_tracker_service())

    def make_services(self) -> AppServices:
        return AppServices(
            users=self.make_user_service(),
            asset_tracker=self.make_asset_tracker_service()
        )

    def make_use_cases(self, services: AppServices | None = None) -> AppUseCases:
        services = services or self.make_services()
        return AppUseCases(
            create_user=CreateUserIfNotExistsUseCase(services.users),
            get_overview=GetAccountOverviewUseCase(services.asset_tracker)
        )