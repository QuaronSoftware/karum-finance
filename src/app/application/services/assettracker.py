import logging
from datetime import datetime, timedelta
from decimal import Decimal
from app.domain.entity import Wallet, Asset, Category, Transaction, TransactionType
from app.shared.safe import safe_execute_coro
from app.application.dto import (
    OverviewDTO,
    OverviewAssetDTO,
    OverviewAssetShortDTO,
    OverviewWalletDTO
)
from app.application.ports import (
    UoWFactory,
    WalletProvider,
    PriceProvider,
    CategoryReader
)
from app.shared.debug import track_time


class AssetTrackerService:
    def __init__(self, uow: UoWFactory, price_provider: PriceProvider, category_reader: CategoryReader, providers: tuple[WalletProvider]):
        self.uow    = uow
        self.price_provider = price_provider
        self.category_reader = category_reader
        self.providers = providers
        self._account_id = 0
        self._logger = logging.getLogger(__name__)
    
    async def get_wallets(self) -> tuple[Wallet, ...]:
        res = []
        for pvdr in self.providers:
            wallets_ids = await pvdr.get_wallets_ids()
            wallets = [await self.get_wallet(a, pvdr.external_id) for a in wallets_ids]

            res += wallets
        return tuple(res)

    async def get_wallet(self, wallet_external_id: str, provider_id: str) -> Wallet:
        async with self.uow as uow:
            name = f"#{wallet_external_id}"
            wallet = Wallet.create(None, name, self._account_id, provider_id, wallet_external_id)
            # If wallet exists then return exists wallet
            # In othercase create new wallet
            wallet = await uow.wallets.create(wallet)

        return wallet

    async def get_overview(self):
        walts = await self.get_wallets()

        # DTO variables
        total_amount = Decimal('0')
        tx_count = 0    # TODO
        wallets = []
        assets = {}

        # processing data
        for w in walts:
            w_amount = Decimal('0')
            asts = []
            wallet_assets = await self.get_assets(w.id)
            for a in wallet_assets:
                # Get variables

                # Special handling for BBSOL (≈ SOL * staking ratio ~1.08)
                # BBSOL is a wrapped staking token on Bybit, not a standard market asset.
                # Its price is derived from SOL via a dynamic staking ratio.
                if a.symbol == 'BBSOL':
                    rate = await self.price_provider.get_rate('SOL') # Get symbol rate price in system currency
                    rate = rate / Decimal('1.08')
                else:
                    rate = await self.price_provider.get_rate(a.symbol) # Get symbol rate price in system currency
                rate_in_usd = Decimal("1") / rate if rate != 0 else 1
                in_usd = a.amount / rate if rate != 0 else a.amount
                total_amount += in_usd
                w_amount+=in_usd

                # Make Asset DTO
                asset_dto = OverviewAssetDTO(symbol=a.symbol, amount=a.amount, ac=in_usd, rate=rate_in_usd, buy_price=Decimal('0'))
                asts.append(asset_dto)
                ast: OverviewAssetShortDTO = assets.get(a.symbol, OverviewAssetShortDTO(symbol=a.symbol, amount=Decimal('0'), ac=Decimal('0'), rate=rate_in_usd))
                ast.amount += a.amount
                ast.ac = ast.amount / rate if rate != 0 else ast.amount
                assets[a.symbol] = ast
            
            # Save in wallets for report
            wallet_dto = OverviewWalletDTO(wallet_provider_name=w.provider_id, wallet_name=w.name, assets=asts, total_amount=w_amount)
            wallets.append(wallet_dto)

        sorted_assets = sorted(list(assets.values()), key=lambda a:a.ac, reverse=True)
        # Combin data to Overview DTO
        response = OverviewDTO(
            tac=total_amount,
            currency=self.price_provider.currency,
            wallets=wallets,
            assets=sorted_assets,
            tx_count=tx_count,
            last_tx=[]
        )
        return response

    async def get_assets(self, wallet_id: int) -> tuple[Asset, ...]:
        """
        Get assets
        """
        txs = await self.get_transactions(wallet_id)

        data = {}

        for tx in txs:
            match tx.type:
                case 'income':
                    if tx.asset.symbol not in data: data[tx.asset.symbol] = Decimal('0')    # type: ignore
                    data[tx.asset.symbol] += tx.asset.amount    # type: ignore
                case 'expense':
                    if tx.asset.symbol not in data: data[tx.asset.symbol] = Decimal('0')    # type: ignore
                    data[tx.asset.symbol] -= tx.asset.amount    # type: ignore

        return tuple(Asset.create(sybmol, amount) for sybmol, amount in data.items() if amount > 0)

    async def get_transactions(self,
                              wallet_id: int,
                              page: int = 0,
                              limit: int = None,
                              start_date: datetime = None,
                              end_date: datetime = None,
                              type: TransactionType = None
                            ) -> tuple[Transaction, ...]:
        """
        Get all transaction

        :param int limit: Result count limits.
        :param int page: Page result, offset by limit.
        :param datetime.date start_date: Start date filtering.
        :param datetime.date end_date: End date filtering.
        :param TransactionType type: Tansaction type. If none then returns all types;
        """
        start_ts = int(start_date.timestamp()) if start_date else None
        end_ts =  int(end_date.timestamp()) if end_date else None
        
        async with self.uow as uow:
            if type is None:
                return await uow.transactions.get_all(wallet_id, start_date=start_ts, end_date=end_ts, page=page, limit=limit)
            else:
                return await uow.transactions.get_all_by_type(wallet_id, type, start_date=start_ts, end_date=end_ts, page=page, limit=limit)


    async def get_all_categories(self) -> tuple[Category, ...]:
        return tuple(await self.category_reader.get_all())

    async def sync_transactions(self, base_start: datetime = None) -> bool:
        now = datetime.now()
        async with self.uow as uow:
            for prdr in self.providers:
                wallets = await uow.wallets.get_all_by_provider_id(prdr.external_id)
                for w in wallets:
                    last_tx = await uow.transactions.get_last(w.id)
                    start_from = last_tx.occurred_at+timedelta(seconds=1) if last_tx else base_start
                    if start_from:
                        txs = await prdr.get_transactions(w.id, w.external_id, start_from, now)
                        if txs:
                            await uow.transactions.create_many(txs)

        return True

    async def add_transactions(self, transactions: list[Transaction]):
        if not transactions: return transactions
        # res = []
    
        async with self.uow as uow:
            return await uow.transactions.create_many(transactions)


    async def close(self):
        """
        Close all connections
        """
        
        for service in self.providers:
            await safe_execute_coro(service.close(), logger=self._logger)
        await safe_execute_coro(self.price_provider.close(), logger=self._logger)
