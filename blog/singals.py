# -*- coding:utf-8  -*-
# @Time     : 2020-7-17 19:10
# @Author   : BGLB
# @Software : PyCharm
from django.db.models.signals import post_save
from django.dispatch import receiver

from bglb_blog.utils import baidu_notify
from blog.models import BlogPost


@receiver(post_save, sender=BlogPost, dispatch_uid="blogpost_post_save")
def my_model_save_handler(sender,instance, created,**kwargs):
    if created and instance.statu == '公开':
        baidu_notify([instance.get_full_url()])

