# -*- coding:utf-8  -*-
# @Time     : 2020-6-10 11:42
# @Author   : BGLB
# @Software : PyCharm

from django.urls import re_path

from blog import views

urlpatterns = [
    # path函数将url映射到视图
    re_path('blog-list/?key=value/', views.blog_list, name='blog_list'),
    re_path('blog-list/', views.blog_list, name='blog_list'),
    re_path('blog-edit/', views.blog_edit, name='blog_edit'),
    re_path('^blog-edit/?id=value$', views.blog_edit, name='blog_edit'),
    re_path('^(?P<username>\w+)$', views.blog_author, name='blog-author'),
    re_path('^blog-detail/(?P<id>\d+)$', views.blog_detail, name='blog-detail'),
    re_path('blog-publish/', views.blog_publish, name='blog_publish'),
    re_path('blog-delete/', views.blog_delete, name='blog_delete'),
    re_path('blog-upimage/', views.blog_image, name='blog_upimage'),
    re_path('blog-click/', views.blog_click, name='blog_click'),

]
