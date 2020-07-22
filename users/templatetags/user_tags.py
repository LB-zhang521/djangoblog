# -*- coding:utf-8  -*-
# @Time     : 2020-7-6 23:22
# @Author   : BGLB
# @Software : PyCharm
from django import template
from users.models import UsersProfile

register = template.Library()


@register.filter
def avatar_url(user_id):
    """
    # 使用:
    获得avatar头像的url
    :param user_id: userid
    """
    try:
        avatar = UsersProfile.objects.get(user_id=user_id).avatar.url
    except:
        avatar = None

    return avatar


@register.filter
def nickname(user_id):
    """
    :param user_id: userid
    """
    nickname = UsersProfile.objects.get(user_id=user_id).nickname
    return nickname


@register.filter
def sign(user_id):
    """
    :param user_id: userid
    """
    sign = UsersProfile.objects.get(user_id=user_id).sign
    return sign


@register.filter
def age(user_id):
    """
    :param user_id: userid
    """
    age = UsersProfile.objects.get(user_id=user_id).age
    return age


@register.filter
def gender(user_id):
    """
    :param user_id: userid
    """
    gender = UsersProfile.objects.get(user_id=user_id).gender
    return gender


@register.filter
def github(user_id):
    """
    :param user_id: userid
    """
    github = UsersProfile.objects.get(user_id=user_id).github
    return github


@register.filter
def qq(user_id):
    """
    :param user_id: userid
    """
    qq = UsersProfile.objects.get(user_id=user_id).qq
    return qq


@register.filter
def telephone(user_id):
    """
    :param user_id: userid
    """
    phone = UsersProfile.objects.get(user_id=user_id).telephone
    return phone


@register.filter
def is_display(user_id):
    """
    :param user_id: userid
    """
    is_display = UsersProfile.objects.get(user_id=user_id).is_display
    return is_display


@register.filter
def occupation(user_id):
    """
    :param user_id: userid
    """
    occupation = UsersProfile.objects.get(user_id=user_id).occupation
    return occupation


@register.filter
def site(user_id):
    """
    :param user_id: userid
    """
    site = UsersProfile.objects.get(user_id=user_id).site
    return site
