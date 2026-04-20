import asyncio
from datetime import datetime
from decimal import Decimal
import logging
from pathlib import Path
from app.config import load_settings
from app.infra.db.engine import build_uow
from app.infra.cache import TTLMemoryCache
from app.infra.price import UniRatePriceProvider, CachePriceProvider
from app.infra.category import JsonCategoryReader
from app.infra.wallets.providers import (
    ByBitExchangeProvider,
    OKXExchangeProvider,
    MonobankProvider
)
from app.application.container import AppContainer
from app.shared.debug import track_time
from app.setup import setup_logging


async def demo():
    settings = load_settings()
    setup_logging(settings.log_level)
    logger = logging.getLogger(__name__)
    category_path = Path('categories.json')

    # providers setup
    cache = TTLMemoryCache()
    category_reader = JsonCategoryReader(category_path)
    database = build_uow(settings.database_url)
    price_provider = UniRatePriceProvider(settings.main_currency, settings.wallets.price_provider_api_key, base_url=settings.wallets.price_provider_base_url)
    bybit = ByBitExchangeProvider(settings.wallets.bybit_api_key, settings.wallets.bybit_secret, base_url=settings.wallets.bybit_base_url)
    okx = OKXExchangeProvider(settings.wallets.okx_api_key, settings.wallets.okx_secret, settings.wallets.okx_passphrase, base_url=settings.wallets.okx_base_url)
    monobank = MonobankProvider(settings.wallets.mono_api_key, base_url=settings.wallets.mono_base_url)

    # Cached providers
    cached_price_provider = CachePriceProvider(price_provider, cache)

    # providers setup
    database = build_uow(settings.database_url)

    # Use case
    container = AppContainer(
        database,
        settings,
        cached_price_provider,
        category_reader=category_reader,
        wallet_providers=(monobank, bybit, okx)
    )
    srvs = container.make_services()
    #use_cases = container.make_use_cases(srvs)

    # Default start
    start = datetime(2025, 1, 1, 0, 0, 0, 0)

    # Transactions sync
    with track_time('sync txs', logger=logger):
        await srvs.asset_tracker.sync_transactions(start)

    # Fetch overview
    with track_time('get asset', logger=logger):
        overview = await srvs.asset_tracker.get_overview()

    # Log out
    print(overview)
    with open('local/overview_test3.json', 'w') as f:
        import json
        json.dump(overview.model_dump(mode='json'), f, indent=4)
    print('Total amount:', f"{overview.tac:.2f}", overview.currency)

    # Close services connections
    await srvs.asset_tracker.close()


asyncio.run(demo())