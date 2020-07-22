# -*- coding:utf-8  -*-
# @Time     : 2020-7-10 23:38
# @Author   : BGLB
# @Software : PyCharm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import strip_tags
from notifications.signals import notify

from comments.models import Comments


@receiver(post_save, sender=Comments)
def send_notification(sender, instance, **kwargs):
    # 发送站内消息
    if instance.parent_comment is None:
        # 评论
        recipient = instance.blog.author
        verb = '评论了你的博文《{0}》'.format(instance.blog.title)
    else:
        recipient = instance.parent_comment.owner
        verb = '回复了你的评论“{0}”'.format(
            strip_tags(instance.parent_comment.content)
        )
    notify.send(instance.owner, recipient=recipient, target=instance.blog, verb=verb, action_object=instance)

