import logging
import asyncio
import random
from typing import TypeVar, Dict, Any, Optional
from pydantic import BaseModel
from aiohttp import (
    ClientSession,
    CookieJar,
    ClientTimeout
)

from .base import BaseSession, RETRYABLE_STATUSES


T = TypeVar('T')


class AiohttpSession(BaseSession):
    def __init__(self,
                 base_url: Optional[str] = None,
                 headers: Optional[dict[str, str]] = None,
                 cookies: Any = None,
                 proxy: Optional[str] = None,
                 logger: logging.Logger | None = None
                ):
        super().__init__(base_url, headers, cookies)
        
        self.timeout = ClientTimeout(self.timeout)
        self._session: ClientSession | None = None
        self._should_reset_connector = True  # flag determines connector state

        # proxy
        self.proxy = proxy
        self._logger = logger or logging.getLogger(__name__)

    async def close(self) -> None:
        if self._session is not None and not self._session.closed:
            await self._session.close()

            # Wait 250 ms for the underlying SSL connections to close
            # https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
            await asyncio.sleep(0.25)
                
    async def create_session(self, headers: Optional[dict] = None, cookies: Optional[dict] = None, timeout: Optional[float] = None) -> ClientSession:
        if self._should_reset_connector:
            await self.close()

        if self._session is None or self._session.closed:
            cookies = cookies or self._cookies

            self._session = ClientSession(
                headers=headers or self._default_headers,
                cookies=cookies if isinstance(cookies, dict) else None,
                cookie_jar=cookies if isinstance(cookies, CookieJar) else None,
                proxy=self.proxy,
                trust_env=False,
                timeout=timeout or self.timeout
            )
            self._should_reset_connector = False

        return self._session

    def build_form_data(self, data: dict) -> dict | None:
        if not data: return None
        result = {}

        for key, value in data.items():
            if value and not key.startswith('__'):
                result[key] = value

        return result
    
    async def fetch_with_retry(self, session: ClientSession,
                           method: str,
                           url: str,
                           *,
                           headers: Optional[dict] = None,
                           params: Optional[dict] = None,
                           body: Optional[dict] = None,
                           retries=3,
                           backoff=1
                           ) -> tuple[bytes | None, int]:
        for attempt in range(retries + 1):
            async with session.request(
                method,
                url,
                headers=headers,
                params=params,
                data=body
            ) as resp:
                # Backoff and retry
                if resp.status in RETRYABLE_STATUSES:
                    sleep_time = backoff * (2 ** attempt) + random.uniform(0, 1)
                    self._logger.warning(f'retry in {sleep_time}; {attempt=}; {url=}')
                    await asyncio.sleep(sleep_time)
                    continue
                
                # Raise for response status code
                resp.raise_for_status()

                # Read body bytes
                data = await resp.read()

                return data, resp.status
        
        # In other case return none
        resp.raise_for_status()
        return None, resp.status

    async def make_request(self,
                           path: str,
                           method: str = 'GET',
                           *, 
                           headers: Optional[dict] = None,
                           params: Optional[dict] = None,
                           body: Optional[dict] = None,
                           timeout: Optional[float] = None,
                           response_model: BaseModel = None
    ):
        # Create session if not exists
        session = await self.create_session(headers=headers, timeout=timeout)

        # Get url and form body
        url = self._api(path)
        form_data = self.build_form_data(body)

        # Fetch
        data, status = await self.fetch_with_retry(
            session, 
            method,
            url,
            headers=headers,
            params=params if method == 'GET' else None,
            body=self._json_dumps(form_data) if isinstance(form_data, dict) else None,
            retries=10,
            backoff=2
        )
        
        # Check response and return response model
        model = self.check_response(status, data, response_model)
        return model

    async def __call__(self,
                       path: str,
                       method: str = 'GET',
                       *, 
                       headers: Optional[dict] = None,
                       params: Optional[dict] = None,
                       body: Optional[dict] = None,
                       timeout: Optional[float] = None,
                       response_model: BaseModel = None
    ):
        return await self.make_request(path, method, headers=headers, params=params, body=body, timeout=timeout, response_model=response_model)

    def set_headers(self, headers: Dict[str, str]):
        self._should_reset_connector = True
        return super().set_headers(headers)
    def set_cookies(self, cookies: Any = None):
        self._should_reset_connector = True
        return super().set_cookies(cookies)
