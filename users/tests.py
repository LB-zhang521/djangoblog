# -*- coding:utf-8  -*-
# @Time     : 2020-6-10 11:45
# @Author   : BGLB
# @Software : PyCharm
import os

import django
import requests
from django.conf import settings
from django.contrib.auth.models import User
import datetime

from notifications.signals import notify

from users.models import UsersProfile

# userPro.avatar = requests.get(url='https://www.baidu.com/img/flexible/logo/pc/result.png')
#
user = User.objects.get(id=16)
#
# print(user)
notify.send(user, recipient=User.objects.filter(is_superuser=True), target=user,
            verb='{}正在注册，验证邮件发送结果{}'.format(user.username, 'true'))
