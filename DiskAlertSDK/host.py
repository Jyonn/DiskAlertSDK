from DiskAlertSDK.entity import Entity


class Host(Entity):
    def __init__(self, name, token, connection):
        super(Host, self).__init__(connection=connection)

        self.name = name
        self.token = token

        self.host = None
        self.auth()

    def auth(self):
        resp = self.post(
            path=f'/api/host/@{self.name}/auth',
            json=dict(token=self.token),
            verify=False,
        )

        self.set_token(resp['token'])
        self.host = resp['host']
        self.verified = True
        return self

    def get_disks(self):
        resp = self.get(
            path=f'/api/host/report/disk',
        )
        return resp

    def create_disks(self, disks):
        resp = self.post(
            path=f'/api/host/report/disk',
            json=dict(disks=disks),
        )
        return resp

    def update_usage(self, disk_name, disk_percentage, folders):
        resp = self.post(
            path=f'/api/host/report/disk/memory',
            json=dict(disk_name=disk_name, disk_percentage=disk_percentage, folders=folders),
        )
        return resp
