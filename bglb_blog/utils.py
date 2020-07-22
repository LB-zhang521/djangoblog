# -*- coding:utf-8  -*-
# @Time     : 2020-7-5 15:53
# @Author   : BGLB
# @Software : PyCharm
import requests

from bglb_blog import settings

import logging

logger = logging.getLogger(__name__)


def baidu_notify(urls):
    try:
        data = '\n'.join(urls)
        result = requests.post(settings.BAIDU_NOTIFY_URL, data=data)
        logger.info(result.content)
        # print(result.content)
    except Exception as e:
        logger.error(e)
