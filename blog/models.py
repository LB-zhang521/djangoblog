# -*- coding:utf-8  -*-
# @Time     : 2020-6-18 11:45
# @Author   : BGLB
# @Software : PyCharm
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from bglb_blog.settings import DOMAIN


class Category(models.Model):
    """
    文章分类
    """
    name = models.CharField(verbose_name='博文分类', max_length=20)

    class Meta:
        verbose_name = '博文分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    文章标签
    """
    name = models.CharField(verbose_name='博文标签', max_length=20)

    class Meta:
        verbose_name = '博文标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """
    博文
    """
    title = models.CharField(verbose_name='标题', max_length=100)
    blog_type = models.CharField(verbose_name='文章类型', max_length=2, default='公开')
    content = models.TextField(verbose_name='正文', default='')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    modify_time = models.DateTimeField(verbose_name='修改时间')
    click_nums = models.IntegerField(verbose_name='浏览量', default=0)
    like = models.IntegerField(verbose_name='点赞数', default=0)
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='文章类别', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='文章标签', blank=True)
    statu = models.CharField(verbose_name='文章状态', default="", max_length=5)

    # 草稿箱 回收站 公开 私密 正在编辑

    class Meta:
        verbose_name = '博文'
        verbose_name_plural = verbose_name
        ordering = ('-create_time',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog-detail', kwargs={
            'id': self.id,
        })

    def get_full_url(self):
        site = DOMAIN
        url = "{site}{path}".format(site=site,
                                    path=self.get_absolute_url())
        return url


class Links(models.Model):
    """友情链接"""

    name = models.CharField('链接名称', max_length=30, unique=True)
    link = models.URLField('链接地址')
    is_enable = models.BooleanField(
        '是否显示', default=True, blank=False, null=False)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Notice(models.Model):
    """公告内容"""
    title = models.CharField('公告标题', max_length=10)
    content = models.CharField('公告正文', max_length=30)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)
    is_enable = models.BooleanField(
        '是否显示', default=True, blank=False, null=False)

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class AD(models.Model):
    """广告内容"""
    title = models.CharField('广告标题', max_length=10)
    content = models.CharField('广告内容', max_length=30)
    img = models.CharField('图片地址', max_length=100)
    ad_link = models.CharField('广告链接', max_length=50)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)
    is_enable = models.BooleanField(
        '是否显示', default=True, blank=False, null=False)

    class Meta:
        verbose_name = '广告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
