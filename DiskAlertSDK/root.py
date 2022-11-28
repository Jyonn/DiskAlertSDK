from DiskAlertSDK.admin import Admin


class Root(Admin):
    def __init__(self, **kwargs):
        super(Root, self).__init__(**kwargs)
        assert self.is_root

    def set_admin(self, user_name, as_admin):
        resp = self.put(
            path='/api/user/',
            json=dict(name=user_name, as_admin=as_admin),
        )
        return resp
