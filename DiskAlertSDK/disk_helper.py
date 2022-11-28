from DiskAlertSDK.admin import Admin
from DiskAlertSDK.connect import Connection
from DiskAlertSDK.host import Host
from DiskAlertSDK.root import Root
from DiskAlertSDK.user import User


class DiskHelper:
    def __init__(self, host='http://localhost:8000'):
        self.connection = Connection(host)

    def user_login(self, name, password):
        return User(name=name, password=password, connection=self.connection)

    def admin_login(self, name, password):
        return Admin(name=name, password=password, connection=self.connection)

    def root_login(self, name, password):
        return Root(name=name, password=password, connection=self.connection)

    def host_login(self, name, token):
        return Host(name=name, token=token, connection=self.connection)
