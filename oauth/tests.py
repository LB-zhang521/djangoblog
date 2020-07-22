import time
from threading import Thread

from django.test import TestCase

# Create your tests here.
from django.core.files import File
from io import BytesIO
from urllib.request import urlopen

from users.models import UsersProfile

use = UsersProfile.objects.get(user_id=23)


def async_my(f):
    """
    异步下载
    :param f:
    :return:
    """

    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


@async_my
def save_avatar(url, img_name):
    try:
        r = urlopen(url)
        io = BytesIO(r.read())
        img = ("{}.jpg".format(img_name), File(io))
    except Exception as e:
        print(e)
        img = None
    return img


temo = save_avatar('https://profile.csdnimg.cn/C/9/A/1_bangenlanbai', 'admin1')
if temo:
    print('s')
    use.avatar = temo
else:
    print("a")
    use.avatar = None
use.save()
