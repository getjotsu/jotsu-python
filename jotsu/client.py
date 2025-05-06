import os


class Jotsu:

    def __init__(self, api_key: str = None):
        self.api_key = api_key if api_key else os.environ['JOTSU_API_KEY']


