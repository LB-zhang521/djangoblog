# -*- coding:utf-8  -*-
# @Time     : 2020-7-5 14:27
# @Author   : BGLB
# @Software : PyCharm

from django.urls import re_path
from . import views

app_name = "comments"
urlpatterns = [
    re_path(r'post/', views.comment_save, name='post_comment'),
    re_path(r'delete/', views.comment_delete, name='delete_comment'),
]
