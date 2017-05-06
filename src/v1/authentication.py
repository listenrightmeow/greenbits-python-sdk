import json
import os
import requests

from django.core.cache import cache
from requests.auth import HTTPBasicAuth

class Authentication():
    @property
    def token(self):
        return cache.get('greenbits/auth/token')

    @token.setter
    def token(self, token):
        cache.set('greenbits/auth/token', token)

    @classmethod
    def preflight(klass, fn):
        def wrapper(self, *args):
            if self.token is None:
                self.me()
            return fn(self, *args)
        return wrapper

    def auth(self):
        return HTTPBasicAuth(os.environ.get('GREENBITS_USERNAME'), os.environ.get('GREENBITS_PASSWORD'))

    def headers(self, token):
        headers = {
            'Authorization': 'Token token="{token}"'.format(token = token)
        }
        return headers

    def me(self):
        try:
            uri = self.uri() + '{path}'.format(path = 'me')
            req = requests.get(uri, auth=self.auth())
        except requests.ConnectionError:
            return None
        else:
            res = self.request(req)
            self.token = res['user']['token']
            return res

    def request(self, res):
        try:
            body = res.json()
        except ValueError:
            return {'message': res.text, 'status_code': res.status_code}
        else:
            body['status_code'] = res.status_code
            return body

    def uri(self, version=1):
        return 'https://api.greenbits.com/api/v{version}/'.format(version=version)
