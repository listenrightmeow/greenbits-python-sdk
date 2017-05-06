import json
import requests
import urllib
import urlparse

from cannabis_menu.menu.data_pipeline.greenbits.v1.authentication import Authentication

class Brands(Authentication):
    def params(self, path):
        tmp = urlparse.urlsplit(path)
        query_params = dict(urlparse.parse_qsl(tmp.query))

        whitelist = [
            'limit',
            'offset',
            'by_name',
            'by_abbreviation',
            'sort_by']

        for key in query_params.iteritems():
            try:
                key in whitelist
            except ValueError:
                raise ValueError('{key} is not a whitelisted parameter'.format(key = key))
            else:
                continue

        return query_params

    @Authentication.preflight
    def brand(self, request, id):
        try:
            path = self.uri() + '{path}/{id}'.format(path = 'brands', id = id)
            req = requests.get(path, headers=self.headers(self.token))
        except requests.ConnectionError:
            return None
        else:
            res = self.request(req)
            return res

    @Authentication.preflight
    def collection(self, request):
        try:
            params = urllib.urlencode(self.params(request.get_full_path()))
            path = self.uri() + '{path}'.format(path = 'brands')
            uri = path + '?{params}'.format(params=params) if params else path
            req = requests.get(uri, headers=self.headers(self.token))
        except requests.ConnectionError:
            return None
        else:
            res = self.request(req)
            return res
