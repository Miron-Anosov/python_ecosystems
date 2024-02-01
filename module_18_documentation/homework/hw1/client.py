import json
import requests


class APIClient:
    TIMEOUT_CONNECT = 5
    URL = 'http://127.0.0.1:'
    _endpoint_authors = '/api/authors'

    singleton = None
    session = None

    def __new__(cls, *args, **kwargs):
        if cls.singleton:
            return cls.singleton
        cls.session = requests.Session()
        cls.singleton = super(APIClient, cls).__new__(cls)
        return cls.singleton

    def get_authors_by_id(self, port: int, id_author: int = 1, ):
        headers = {'Connection': 'keep-alive'}
        url = f'{self.URL}{port}{self._endpoint_authors}/{id_author}'

        return self.session.get(url=url, timeout=self.TIMEOUT_CONNECT, headers=headers).json()

    def post_authors(self, json_ob: json):
        url = f'{self.URL}{self._endpoint_authors}'
        return self.session.post(url=url, json=json_ob,
                                 timeout=self.TIMEOUT_CONNECT).json()


def get_authors_by_id_without_session(port: int):
    return requests.get(f'http://127.0.0.1:{port}/api/authors/1')
