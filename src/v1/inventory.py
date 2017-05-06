import json
import requests
import urllib
import urlparse

from cannabis_menu.menu.data_pipeline.greenbits.v1.authentication import Authentication

class Inventory(Authentication):
    def params(self, path):
        tmp = urlparse.urlsplit(path)
        query_params = dict(urlparse.parse_qsl(tmp.query))

        whitelist = [
            'limit',
            'offset',
            'sellable',
            'only_assigned',
            'by_sku',
            'by_lot_number',
            'by_product_id',
            'by_product_name']

        for key in query_params.iteritems():
            try:
                key in whitelist
            except ValueError:
                raise ValueError('{key} is not a whitelisted parameter'.format(key = key))
            else:
                continue

        return query_params

    # @Authentication.preflight
    def item(self, request, id):
        try:
            path = self.uri() + '{path}/{id}'.format(path = 'inventory_items', id = id)
            return { 'path': path, 'status_code': 200 }
            req = requests.get(path, headers=self.headers(self.token))
        except requests.ConnectionError:
            return None
        else:
            res = self.request(req)
            return res

    @Authentication.preflight
    def items(self, request):
        try:
            params = urllib.urlencode(self.params(request.get_full_path()))
            path = self.uri() + '{path}'.format(path = 'inventory_items')
            uri = path + '?{params}'.format(params=params) if params else path
            req = requests.get(uri, headers=self.headers(self.token))
        except requests.ConnectionError:
            return None
        else:
            res = self.request(req)
            return res
