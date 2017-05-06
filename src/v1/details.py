import requests

from cannabis_menu.menu.data_pipeline.greenbits.v1.authentication import Authentication

class Details(Authentication):
    @Authentication.preflight
    def companies(self, id):
        try:
            uri = self.uri() + '{path}/{id}'.format(path='companies', id=id)
            req = requests.get(uri, headers=self.headers(self.token))
        except requests.ConnectionError:
            return None
        else:
            return self.request(req)
