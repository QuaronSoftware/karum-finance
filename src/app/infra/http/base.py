import json
from abc import ABC, abstractmethod
from typing import Callable, Any, TypeVar, Optional
from pydantic import BaseModel, TypeAdapter


_JsonLoads = Callable[..., Any]
_JsonDumps = Callable[..., str]

T = TypeVar('T')
DEFAULT_TIMEOUT: float = 60.0
RETRYABLE_STATUSES = (408, 425, 429, 500, 502, 503, 504)


class BaseSession(ABC):
    def __init__(self,
                 base_url: Optional[str] = None,
                 headers: Optional[dict] = None,
                 cookies: Any = None,
                 json_loads: _JsonLoads = json.loads,
                 json_dumps: _JsonDumps = json.dumps,
                 timeout: float = DEFAULT_TIMEOUT
        ):
        if isinstance(base_url, str):
            base_url = base_url.rstrip('/')

        self.timeout = timeout
        self._base_url = base_url
        self._cookies = cookies
        self._default_headers = headers or {}

        self._json_loads = json_loads
        self._json_dumps = json_dumps
    
    def _api(self, url: str):
        if url.startswith('http://') or url.startswith('https://'):
            return url
        return f"{self._base_url}{url}"


    @abstractmethod
    async def make_request(self,
                           path: str,
                           method: str = 'GET',
                           *, 
                           headers: Optional[dict] = None,
                           params: Optional[dict] = None,
                           body: Optional[dict] = None,
                           timeout: Optional[float] = None,
                           response_model: T = None
    ) -> T:
        """
        Make request to API Server by method name

        :param str method: HTTP Method name
        :param str url: API URL
        :param dict params: Query params
        :param dict body: Request body
        :param float timeout: Timeout
        """
        ...
    
    @abstractmethod
    async def close(self) -> None:  # pragma: no cover
        """
        Close client session
        """

    def check_response(self, status_code: int, content: str | bytes, response_type: BaseModel) -> BaseModel | None:
        """
        Check response

        :param int status_code: HTTP request status code
        :param str content: Response body content
        """

        #if 200 <= status_code <= 299:
        #    return None
        
        if status_code==204:
            # Status code 204 not provide for response content
            return None

        try:
            json_data = self._json_loads(content)
        except Exception as e:  # noqa: BLE001
            # Handled error type can't be classified as specific error
            # in due to decoder can be customized and raise any exception

            msg = "Failed to decode object"
            raise Exception(msg, e, content[:4096]) from e
        
        model = TypeAdapter(response_type).validate_python(json_data)
        return model
    
    def set_headers(self, headers: dict[str, str]):
        self._default_headers=headers
    
    def set_cookies(self, cookies: Any = None):
        self._cookies = cookies


