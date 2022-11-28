from DiskAlertSDK.connect import Connection
from DiskAlertSDK.entity import Entity


class ChannelStatus:
    WAIT_BIND = 0
    WAIT_CAPTCHA = 1
    ACTIVATED = 2


class Channel:
    def __init__(self, user, channel_name):
        self.user = user
        self.channel_name = channel_name

    @property
    def is_waiting_bind(self):
        return self.status == ChannelStatus.WAIT_BIND

    def is_waiting_captcha(self):
        return self.status == ChannelStatus.WAIT_CAPTCHA

    def is_activated(self):
        return self.status == ChannelStatus.ACTIVATED

    @property
    def status(self):
        return self.user.get_property(f'{self.channel_name}_status')

    @property
    def silent(self):
        return self.user.get_property(f'{self.channel_name}_silent')

    def bind(self, value):
        resp = self.user.put(
            path=f'/api/user/{self.channel_name}',
            json={self.channel_name: value},
        )
        self.user.user = resp
        return self.user

    def verify(self, captcha):
        resp = self.user.put(
            path=f'/api/user/{self.channel_name}/captcha',
            json={f'{self.channel_name}_captcha': str(captcha)},
        )
        self.user.user = resp
        return self.user

    def set_silent(self, silent):
        resp = self.user.put(
            path=f'/api/user/{self.channel_name}',
            json=dict(silent=silent),
        )
        self.user.user = resp
        return self.user


class UserDisk:
    def __init__(self, host, disk_name):
        self.host = host
        self.disk_name = disk_name
        self.disk = None

    def about(self):
        resp = self.host.user.get(
            path=f'/api/host/{self.host.host_name}/userdisk',
        )
        self.disk = resp
        return self

    def set_bind(self, bind):
        resp = self.host.user.put(
            path=f'/api/host/{self.host.host_name}/userdisk',
            json=dict(bind=bind),
        )
        self.disk = resp
        return self

    def set_percentage(self, percentage):
        resp = self.host.user.put(
            path=f'/api/host/{self.host.host_name}/userdisk/percentage',
            json=dict(percentage=percentage),
        )
        self.disk = resp
        return self


class UserHost:
    def __init__(self, user, host_name):
        self.user = user
        self.host_name = host_name

        self.host = None
        self.Disk = lambda disk_name: UserDisk(self, disk_name)

    def about(self):
        resp = self.user.get(
            path=f'/api/host/{self.host_name}',
        )
        self.host = resp
        return resp

    def get_disks(self):
        resp = self.user.get(
            path=f'/api/host/{self.host_name}/disk',
        )
        return resp


class User(Entity):
    def __init__(self, name: str, password: str, connection: Connection):
        super(User, self).__init__(connection=connection)

        self.name = name
        self.password = password

        self.phone = Channel(self, 'phone')
        self.email = Channel(self, 'email')
        self.bark = Channel(self, 'bark')

        self.user = None
        self.auth()

        self.Host = lambda host_name: UserHost(self, host_name)

    def get_property(self, key):
        if self.user:
            return self.user.get(key, None)

    @property
    def is_root(self):
        return self.get_property('root')

    @property
    def is_admin(self):
        return self.get_property('admin')

    def auth(self):
        resp = self.post(
            path=f'/api/user/{self.name}',
            json=dict(password=self.password),
            verify=False,
        )

        self.set_token(resp['token'])
        self.user = resp['user']
        self.verified = True
        return self

    def about(self):
        resp = self.get(
            path='/api/user/me',
        )
        self.user = resp
        return resp

    def set_silent(self, silent):
        resp = self.post(
            path='/api/user/me',
            json=dict(silent=silent),
        )
        self.user = resp
        return self

    def modify_password(self, password):
        resp = self.put(
            path='/api/user/me',
            json=dict(password=password),
        )
        self.user = resp
        return self

    def get_hosts(self):
        resp = self.get(
            path='/api/host/',
        )
        return resp

    def update_disk_alert_percentage(self, host_name, disk_name, alert_percentage):
        resp = self.put(
            path=f'/api/host/{host_name}/userdisk/percentage',
            json=dict(name=disk_name, alert_percentage=alert_percentage),
        )
        return resp

    def update_disk_bind(self, host_name, disk_name, bind):
        resp = self.put(
            path=f'/api/host/{host_name}/userdisk/bind',
            json=dict(name=disk_name, bind=bind),
        )
        return resp
