# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as tran


class OAuthUser(models.Model):
    user = models.OneToOneField(User, verbose_name='用户',
                                on_delete=models.CASCADE)
    openid = models.CharField(max_length=50)

    token = models.CharField(max_length=150, null=True, blank=True)

    type = models.CharField(blank=False, null=False, max_length=50)

    userdata = models.TextField(null=True, blank=True)

    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    last_mod_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'oauth用户'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']


class OAuthConfig(models.Model):
    oauth_type_choices = (
        ('github', 'GitHub'),
        ('qq', 'QQ'),
    )

    oauth_type = models.CharField('类型', max_length=10, choices=oauth_type_choices, default='a')
    appkey = models.CharField(max_length=200, verbose_name='AppKey')
    appsecret = models.CharField(max_length=200, verbose_name='AppSecret')
    callback_url = models.CharField(
        max_length=200,
        verbose_name='回调地址',
        blank=False,
        default='http://www.baidu.com')
    is_enable = models.BooleanField(
        '是否显示', default=True, blank=False, null=False)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    mod_time = models.DateTimeField('修改时间', auto_now=True)

    def clean(self):
        if OAuthConfig.objects.filter(
                oauth_type=self.oauth_type).exclude(id=self.id).count():
            raise ValidationError(tran(self.oauth_type+'已经存在'))

    def __str__(self):
        return self.oauth_type

    class Meta:
        verbose_name = 'oauth管理'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
