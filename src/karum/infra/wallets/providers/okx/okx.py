import asyncio
import base64
import hashlib
import hmac
from datetime import datetime, UTC

import urllib.parse

from karum.infra.http import AiohttpSession, BaseSession
from .models import OKXBillResponse, OKXBill, OKXAccountBillResponse


class OKXExchangeClient:
    def __init__(self, api_key: str, secret: str, passphrase: str, *, base_url: str = None, client: BaseSession = None):
        self._client = client or AiohttpSession(base_url)
        self._api_key = api_key
        self._secret = secret
        self._passphrase = passphrase
    
    def _gen_signature(self, time_stamp: str, method: str, path: str):
        param_str = f"{time_stamp}{method}{path}"
        hash = base64.b64encode(hmac.new(bytes(self._secret, "utf-8"), param_str.encode("utf-8"), hashlib.sha256).digest())
        signature = hash.decode('utf-8')
        return signature
    
    def _build_headers(self, method: str, path: str, payload):
        now = datetime.now(UTC)
        timeiso = now.isoformat(timespec='milliseconds').replace('+00:00', '') + 'Z'
        path += ('?' + payload) if payload else ''
        return {
            'OK-ACCESS-KEY': self._api_key,
            'OK-ACCESS-TIMESTAMP': timeiso,
            'OK-ACCESS-SIGN' : self._gen_signature(timeiso, method, path),
            'OK-ACCESS-PASSPHRASE': self._passphrase,
            'Content-Type': 'application/json'
        }

    async def _fetch_funding_history(self, start_date: int = None, end_date: int = None, limit: int = 100):
        path = '/api/v5/asset/bills-history'
        payload = {'limit': str(limit)}
        if start_date is not None:
            payload['before'] = str(start_date)
        if end_date is not None:
            payload['after'] = str(end_date)

        headers = self._build_headers('GET', path, urllib.parse.urlencode(payload))

        # Fetch data
        resp = await self._client.make_request(path, headers=headers, params=payload, response_model=OKXBillResponse)

        return resp
    
    async def _fetch_unified_history(self, start_date: int = None, end_date: int = None, limit: int = 100):
        path = '/api/v5/account/bills-archive'
        payload = {'limit': str(limit)}
        if start_date is not None:
            payload['begin'] = str(start_date)
        if end_date is not None:
            payload['end'] = str(end_date)

        headers = self._build_headers('GET', path, urllib.parse.urlencode(payload))

        # Fetch data
        resp = await self._client.make_request(path, headers=headers, params=payload, response_model=OKXAccountBillResponse)

        return resp

    async def _fetch_all_funding_history(self, start_date: int = None, end_date: int = None):
        transactions: list[OKXBill] = []
        STEP = 2_678_400 * 1000
        current_from = start_date
        current_to = current_from + STEP

        while current_from < end_date:
            current_to = min(current_from + STEP, end_date)

            response = await self._fetch_funding_history(current_from, current_to)
            transactions.extend(response.data)

            current_from = response.data[0].timestamp if response.data else current_to
            await asyncio.sleep(1)  # rate limit safety
        
        return transactions

    async def close(self) -> None:
        return await self._client.close()


