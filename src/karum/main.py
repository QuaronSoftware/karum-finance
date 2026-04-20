import logging
from karum.config import load_settings
from karum.delivery.fastapi import create_app
from karum.infra.db.engine import build_uow
from karum.infra.cache import TTLMemoryCache
from karum.infra.category import JsonCategoryReader
from karum.infra.price import UniRatePriceProvider, CachePriceProvider
from karum.infra.wallets.providers import (
    ByBitExchangeProvider,
    OKXExchangeProvider,
    MonobankProvider
)
from karum.application.container import AppContainer
from .setup import setup_logging


def main():
    settings = load_settings()
    setup_logging(settings.log_level)
    logger = logging.getLogger(__name__)

    # providers setup
    cache = TTLMemoryCache()
    database = build_uow(settings.database_url)
    category_reader = JsonCategoryReader(settings.category_path)
    price_provider = UniRatePriceProvider(settings.main_currency, settings.wallets.price_provider_api_key, base_url=settings.wallets.price_provider_base_url)
    bybit = ByBitExchangeProvider(settings.wallets.bybit_api_key, settings.wallets.bybit_secret, base_url=settings.wallets.bybit_base_url)
    okx = OKXExchangeProvider(settings.wallets.okx_api_key, settings.wallets.okx_secret, settings.wallets.okx_passphrase, base_url=settings.wallets.okx_base_url)
    monobank = MonobankProvider(settings.wallets.mono_api_key, base_url=settings.wallets.mono_base_url)

    # Cached providers
    cached_price_provider = CachePriceProvider(price_provider, cache)

    # Setup
    app = create_app()

    # providers setup
    database = build_uow(settings.database_url)

    # Use case
    container = AppContainer(
        database,
        settings,
        cached_price_provider,
        category_reader=category_reader,
        wallet_providers=(bybit, okx, monobank)
    )
    app.state.container = container

    return app
