# -*- coding:utf-8  -*-
# @Time     : 2020-6-10 11:42
# @Author   : BGLB
# @Software : PyCharm
from django.urls import re_path
from . import views

app_name = 'users'
urlpatterns = [
    # re_path和path的作用都是一样的。只不过re_path是在写url的时候可以用正则表达式，功能更加强大。
    re_path(r'reg/', views.user_reg, name='reg'),
    re_path(r'login/', views.user_login, name='login'),
    re_path(r'profile/', views.profile, name='profile'),
    re_path(r'logout/', views.user_logout, name='logout'),
    re_path(r'update_password/', views.update_password, name='update_password'),
    re_path(r'reset_password/', views.reset_password, name='reset_password'),
    re_path(r'update_email/', views.update_email, name='update_email'),
    re_path(r'email_result/', views.email_result, name='email_result'),
    re_path(r'activate/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/', views.activate, name='activate_result'),
]
