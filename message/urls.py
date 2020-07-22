# -*- coding:utf-8  -*-
# @Time     : 2020-7-5 14:27
# @Author   : BGLB
# @Software : PyCharm

from django.urls import re_path
from . import views

app_name = "message"
urlpatterns = [
    # re_path和path的作用都是一样的。只不过re_path是在写url的时候可以用正则表达式，功能更加强大。
    re_path(r'list/', views.show_message, name='message-list'),
    re_path(r'update/', views.update_message, name='message-update'),
]
