import os

import httpx
from httpx import URL, Response


class Jotsu(httpx.Client):

    def __init__(self, *, account_id: str = None, api_key: str = None, base_url: str = None):
        super().__init__()
        self.base_url = base_url if base_url else os.getenv('JOTSU_API_URL') or 'https://api.jotsu.com'
        self.account_id = account_id if account_id else os.environ['JOTSU_ACCOUNT_ID']
        self.api_key = api_key if api_key else os.environ['JOTSU_API_KEY']

    def _parse_url(self, url: str) -> str:
        if url.startswith('/'):
            return f'{self.base_url}{url}'
        return url

    def request(
        self,
        method: str,
        url: URL | str,
        **kwargs
    ) -> Response:
        url = self._parse_url(url)

        headers = kwargs.pop('headers') or {}
        assert isinstance(headers, dict)
        headers['Authorization'] = f'Bearer {self.api_key}'

        return super().request(method, url, headers=headers, **kwargs)
