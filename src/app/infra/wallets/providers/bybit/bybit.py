import hmac
import hashlib
from decimal import Decimal
from urllib.parse import urlencode

from typing import Literal, get_args
from app.infra.http import AiohttpSession, BaseSession
from app.shared.time import current_milli_time
from .models import TransactionItem, BybitFundingHistoryResponse


ACCOUNTTYPE = Literal['UNIFIED', 'FUND']


class ByBitExchangeClient:
    def __init__(self, api_key: str, secret: str, *, base_url: str = None, client: BaseSession = None):
        self._client = client or AiohttpSession(base_url)
        self._api_key = api_key
        self._secret = secret
    
    def _gen_signature(self, time_stamp: str, recv_window, payload):
        param_str = f"{time_stamp}{self._api_key}{recv_window}{payload}"
        hash = hmac.new(bytes(self._secret, "utf-8"), param_str.encode("utf-8"),hashlib.sha256)
        signature = hash.hexdigest()
        return signature
    
    def _build_headers(self, payload):
        time_stamp = str(current_milli_time())
        recv_window = 5000
        return {
            'X-BAPI-API-KEY': self._api_key,
            'X-BAPI-TIMESTAMP': time_stamp,
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-RECV-WINDOW': str(recv_window),
            'X-BAPI-SIGN' : self._gen_signature(time_stamp, recv_window, payload),
            'Content-Type': 'application/json'
        }

    async def _fetch_funding_history(self, start_date: int = None, end_date: int = None, cursor: str = None, limit: int = 50) -> BybitFundingHistoryResponse:
        path = '/v5/asset/fundinghistory'
        payload = {'limit': limit}

        if start_date is not None:
            payload['createTimeFrom'] = start_date
        if end_date is not None:
            payload['createTimeTo'] = end_date
        if cursor is not None:
            payload['cursor'] = cursor

        headers = self._build_headers(urlencode(payload, safe=','))
        resp = await self._client.make_request(path, headers=headers, params=payload, response_model=BybitFundingHistoryResponse)
        return resp     # type: ignore
    
    async def _fetch_transactions(self, start_date: int = None, end_date: int = None):
        transactions: list[TransactionItem] = []
        TIME_RANGE = 590_400    # 6.8 days (limit up to 7 days)
        current_from = start_date

        while current_from < end_date:
            current_to = min(current_from + TIME_RANGE, end_date)
            response = await self._fetch_funding_history(current_from, current_to, None, 50)

            if response: transactions.extend(response.result.list)
            
            current_from = current_to
        
        return transactions

    def get_account_wallets_names(self):
        return get_args(ACCOUNTTYPE)

    async def close(self) -> None:
        return await self._client.close()
