# -*- coding:utf-8  -*-
# @Time     : 2020-7-6 21:29
# @Author   : BGLB
# @Software : PyCharm
import math
from django import template

from django.utils import timezone

from blog.models import Category, Links, Notice, AD

register = template.Library()


@register.inclusion_tag('blog/blog_category.html')
def categorys():
    categorys = Category.objects.values("id", "name")

    return {"categorys": categorys}


@register.filter()
def blog_original_count(bloglist):
    count = 0
    for blog in bloglist:
        if blog.blog_type == "原创":
            count += 1
    return count


@register.filter()
def blog_click_count(bloglist):
    count = 0
    for blog in bloglist:
        count += blog.click_nums
    return count


@register.filter()
def blog_like_count(bloglist):
    count = 0
    for blog in bloglist:
        count += blog.like
    return count


@register.filter()
def blog_pub_time(_time):
    now = timezone.now()
    ret = now-_time
    if ret.days == 0:
        if ret.seconds <= 60:
            ret = str(ret.seconds)+"秒前"
        elif ret.seconds <= 3600:
            ret = str(math.floor(ret.seconds/60))+"分钟前"
        else:
            ret = str(math.floor(ret.seconds/3600))+"小时前"

    elif ret.days < 30:
        ret = str(ret.days)+"天前"

    elif ret.days < 365:
        ret = str(math.floor(ret.days/30))+"月前"
    else:
        ret = str(math.floor(ret.days/365))+"年前"
    return ret


@register.inclusion_tag('blog/tags/links.html')
def links_friend():
    links = Links.objects.filter(is_enable=True).all()
    return {"links": links}


@register.inclusion_tag('blog/tags/notice.html')
def notice():
    notice = Notice.objects.filter(is_enable=True).all()
    return {"notice": notice}


@register.inclusion_tag('blog/tags/AD.html')
def ADTag():
    ad = AD.objects.filter(is_enable=True).all()
    return {"AD": ad}
