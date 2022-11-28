import requests


class Connection:
    def __init__(self, host: str):
        if host.endswith('/'):
            host = host[:-1]
        self.host = host

    @staticmethod
    def unpack(req):
        try:
            resp = req.json()
        except Exception as e:
            raise ConnectionError(f'Unpack error: {e}')
        if resp['code'] != 0:
            msg = resp['msg']
            if resp['append_msg']:
                msg += f': {resp["append_msg"]}'
            raise ConnectionError(f'Response error: {msg}')
        return resp['body']

    @staticmethod
    def get_header(token):
        if not token:
            return None
        return {
            'Token': token,
        }

    def get(self, path, params=None, token=None):
        headers = self.get_header(token)
        with requests.get(url=f'{self.host}{path}', params=params, headers=headers) as req:
            return self.unpack(req)

    def post(self, path, json=None, token=None):
        headers = self.get_header(token)
        with requests.post(url=f'{self.host}{path}', json=json, headers=headers) as req:
            return self.unpack(req)

    def put(self, path, json=None, token=None):
        headers = self.get_header(token)
        with requests.put(url=f'{self.host}{path}', json=json, headers=headers) as req:
            return self.unpack(req)

    def delete(self, path, json=None, token=None):
        headers = self.get_header(token)
        with requests.delete(url=f'{self.host}{path}', json=json, headers=headers) as req:
            return self.unpack(req)

