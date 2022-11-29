from DiskAlertSDK.user import User, UserHost, UserDisk


class AdminDisk(UserDisk):
    def set_listen(self, listen):
        resp = self.host.user.put(
            path=f'/api/host/@{self.host.host_name}/disk/@{self.disk_name}',
            json=dict(listen=listen),
        )
        self.disk = resp
        return self

    def delete(self):
        resp = self.host.user.delete(
            path=f'/api/host/@{self.host.host_name}/disk/@{self.disk_name}',
        )
        return resp


class AdminHost(UserHost):
    def __init__(self, user, host_name):
        super(AdminHost, self).__init__(user=user, host_name=host_name)

        self.Disk = lambda disk_name: AdminDisk(self, disk_name)

    def create(self, internal_ip):
        resp = self.user.post(
            path=f'/api/host/@{self.host_name}',
            json=dict(internal_ip=internal_ip),
        )
        self.host = resp
        return resp

    def set_silent(self, silent):
        resp = self.user.put(
            path=f'/api/host/@{self.host_name}',
            json=dict(silent=silent),
        )
        self.host = resp
        return self

    def delete(self):
        resp = self.user.delete(
            path=f'/api/host/@{self.host_name}',
        )
        return resp


class Admin(User):
    def __init__(self, **kwargs):
        super(Admin, self).__init__(**kwargs)
        assert self.is_admin or self.is_root

        self.Host = lambda host_name: AdminHost(self, host_name)

    def get_users(self):
        resp = self.get(
            path='/api/user/',
        )
        return resp

    def create_user(self, name):
        resp = self.post(
            path='/api/user/',
            json=dict(name=name),
        )
        return resp

    def get_user(self, user_name):
        resp = self.get(
            path=f'/api/user/@{user_name}',
        )
        return resp

    def delete_user(self, user_name):
        resp = self.delete(
            path=f'/api/user/@{user_name}',
        )
        return resp

