# -*- coding:utf-8  -*-
# @Time     : 2020-7-11 13:29
# @Author   : BGLB
# @Software : PyCharm
from django.utils.html import strip_tags
from notifications.signals import notify


def send_notification(instance, **kwargs):
    """发送站内消息"""
    if instance.parent_comment is None:
        # 评论
        recipient = instance.blog.author
        verb = '评论了你的博文《{0}》'.format(instance.blog.title)
    else:
        recipient = instance.parent_comment.owner
        verb = '回复了你的评论“{0}”'.format(
            strip_tags(instance.parent_comment.content)
        )
    if instance.owner != instance.blog.author:
        notify.send(instance.owner, recipient=recipient, target=instance.blog, verb=verb, action_object=instance)
