from DiskAlertSDK.connect import Connection


class Entity:
    def __init__(self, connection: Connection):
        self.connection = connection
        self._token = None
        self.verified = False

    def set_token(self, token):
        self._token = token
        return self

    def get(self, path, params=None, verify=True):
        if verify and not self._token:
            raise ConnectionError('Not authorized')
        return self.connection.get(path, params, self._token)

    def post(self, path, json=None, verify=True):
        if verify and not self._token:
            raise ConnectionError('Not authorized')
        return self.connection.post(path, json, self._token)

    def put(self, path, json=None, verify=True):
        if verify and not self._token:
            raise ConnectionError('Not authorized')
        return self.connection.put(path, json, self._token)

    def delete(self, path, json=None, verify=True):
        if verify and not self._token:
            raise ConnectionError('Not authorized')
        return self.connection.delete(path, json, self._token)

    def auth(self):
        raise NotImplementedError
