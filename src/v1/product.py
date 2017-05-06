import json
import requests
import urllib
import urlparse

from cannabis_menu.menu.data_pipeline.greenbits.v1.authentication import Authentication

class Product(Authentication):
    def params(self, path):
        tmp = urlparse.urlsplit(path)
        query_params = dict(urlparse.parse_qsl(tmp.query))

        whitelist = [
            'limit',
            'offset',
            'active',
            'by_active',
            'mj',
            'para',
            'by_name',
            'by_vendor',
            'by_category',
            'by_sku',
            'by_lot_number',
            'by_product_number',
            'by_brand',
            'by_strain',
            'by_discountable']

        for key in query_params.iteritems():
            try:
                key in whitelist
            except ValueError:
                raise ValueError('{key} is not a whitelisted parameter'.format(key = key))
            else:
                continue

        return query_params

    @Authentication.preflight
    def product(self, request, id):
        try:
            path = self.uri() + '{path}/{id}'.format(path = 'products', id = id)
            req = requests.get(path, headers=self.headers(self.token))
        except requests.ConnectionError:
            return None
        else:
            res = self.request(req)
            return res

    @Authentication.preflight
    def products(self, request):
        try:
            params = urllib.urlencode(self.params(request.get_full_path()))
            path = self.uri() + '{path}'.format(path = 'products')
            uri = path + '?{params}'.format(params=params) if params else path
            req = requests.get(uri, headers=self.headers(self.token))
        except requests.ConnectionError:
            return None
        else:
            res = self.request(req)
            return res

    @Authentication.preflight
    def types(self, request):
        try:
            path = self.uri() + '{path}'.format(path = 'product_types')
            req = requests.get(path, headers=self.headers(self.token))
        except requests.ConnectionError:
            return None
        else:
            res = self.request(req)
            return res
