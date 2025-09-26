import os
from wsgiref.headers import Headers

import httpx
from httpx import URL, Response


class Jotsu(httpx.Client):

    def __init__(self, *, api_key: str = None, **kwargs):
        base_url = kwargs.pop('base_url', os.getenv('JOTSU_API_URL') or 'https://api.jotsu.com')
        self.api_key = api_key if api_key else os.environ['JOTSU_API_KEY']

        headers = httpx.Headers(kwargs.pop('headers', {}))
        if not 'Authorization' in headers:
            headers['Authorization'] = f'Bearer {self.api_key}'

        super().__init__(base_url=base_url, headers=headers, **kwargs)
