# DiskAlertSDK

磁盘空间监控SDK，当磁盘超过阈值时，会发送邮件、短信、Bark通知。

## 1. 介绍

存在超级管理员，管理员和普通用户三种角色。

- 当监控的磁盘空间超过阈值（默认80%）时，会给所有管理员发送预警通知及详细使用情况。
- 当磁盘某一用户空间超过一定阈值（默认10%）时，会给这一用户发送预警通知。

强烈推荐安装Bark，可以在手机上收到通知。暂时只支持[iOS](https://apps.apple.com/cn/app/bark-%E7%BB%99%E4%BD%A0%E7%9A%84%E6%89%8B%E6%9C%BA%E5%8F%91%E6%8E%A8%E9%80%81/id1403753865)。

### 用户

- 强烈建议用户在首次登录后修改密码。
- 用户可以绑定一个邮箱、一个手机号码以及一个Bark推送码，用于接收预警通知。
- 用户可以对自动绑定的磁盘进行解绑。
- 用户可以对绑定的磁盘设置预警阈值（如从10%降到5%）。
- 用户可以将邮箱、手机号码、Bark推送码设置为不接收预警通知。

### 管理员

- 管理员可以设置普通用户账户。
- 管理员可以添加新监控主机，删除或编辑主机预警阈值。
- 管理员可以设置主机的磁盘预警阈值和监控状态（是否监控）。

### 超级管理员

- 超级管理员可以设置管理员账户。

## 2. 安装

```bash
pip install DiskAlertSDK
```

## 3. 服务端部署（适用于超级管理员，管理员和普通用户忽略）

### 项目部署

配置[LabDiskAlert](https://github.com/Jyonn/LabDiskAlert)项目。
可以搭配[NotificatorX](https://github.com/Jyonn/NotificatorX)的中央通知服务。

下文均假设主机为`https://alert.abc.com`。
需提前在`User_user`表中添加超级管理员（root）账号。

### 添加用户并设置为管理员

```python
from DiskAlertSDK import DiskHelper

helper = DiskHelper(host='https://alert.abc.com')
root = helper.root_login(name='root', password='password')

root.create_user(name='admin')  # 添加用户，初始密码和用户名相同
root.set_admin(name='admin', as_admin=True)  # 设置用户为管理员
```

## 4. 主机管理（适用于管理员，普通用户忽略）

```python
from DiskAlertSDK import DiskHelper

helper = DiskHelper(host='https://alert.abc.com')
admin = helper.admin_login(name='admin', password='admin')

admin.modify_password('admin123')  # 强烈建议修改密码
[admin.create_user(name=name) for name in ['user1', 'user2', 'user3']]  # 添加用户

host = admin.Host('CPU')  # 指定主机名
host.create(internal_ip='192.168.12.168')  # 添加名为CPU的主机，IP为192.168.12.168。均可以随意设置，只是为了用户可读性。

# 在主机添加本项目完成初始化后，通过如下方式添加磁盘监控
disk = host.Disk('home')  # 指定磁盘名
disk.set_listen(True)  # 设置对/home目录进行监听
disk.set_percentage(50)  # 设置磁盘使用率阈值为50%，超过将发送预警通知
```

## 5. 用户初始化

```python
from DiskAlertSDK import DiskHelper

# 连接服务器
helper = DiskHelper(host='https://alert.abc.com')
user = helper.user_login(name='user1', password='user1')  # 登录
user.modify_password('user123')  # 强烈建议修改密码

user.email.bind('user1@abc.com')  # 绑定邮箱
user.email.verify('893246')  # 验证邮箱，输入邮箱收到的六位验证码

user.phone.bind('+85212341234')  # 绑定手机号码
user.phone.verify('893246')  # 验证手机号码，输入手机收到的六位验证码

user.bark.bind('https://api.day.app/xxxxxxxxxxxxxxxxx')  # 绑定Bark推送码
user.bark.verify('893246')  # 验证Bark推送码，输入Bark收到的六位验证码

user.Host('CPU').Disk('home').set_percentage(5)  # 设置CPU:/home磁盘的用户使用率阈值为5%，超过将发送预警通知
user.Host('CPU').Disk('home').set_bind(False)  # 设置用户不接收CPU:/home磁盘使用率预警通知
```
