# -*- coding:utf-8  -*-
# @Time     : 2020-6-10 11:45
# @Author   : BGLB
# @Software : PyCharm

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class UsersProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_id')
    nickname = models.CharField(max_length=255, default="昵称", verbose_name="用户昵称")
    age = models.IntegerField(default=18, verbose_name="用户年龄")
    gender = models.CharField(max_length=2, default="男", verbose_name="性别")
    telephone = models.CharField('电话', max_length=11, blank=True, )
    # 最后修改时间
    mod_date = models.DateTimeField('最后修改信息时间', auto_now=True)
    # 头像
    avatar = models.ImageField('用户头像', upload_to='avatar/', default="avatar/default.jpg", blank=True)
    sign = models.TextField(max_length=500, blank=True)  # 个性签名
    qq = models.CharField(max_length=12, verbose_name='qq', blank=True)
    github = models.CharField(max_length=100, verbose_name='github', blank=True)
    site = models.CharField(max_length=100, verbose_name='个人网站', blank=True)
    is_display = models.BooleanField(verbose_name='是否展示个人信息', default=False)
    occupation = models.CharField(verbose_name='身份', default='个人开发者', max_length=15)

    class Meta:
        verbose_name = '用户基本信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.__str__()


@receiver(pre_delete, sender=UsersProfile)
def avatar_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.avatar.delete(False)
