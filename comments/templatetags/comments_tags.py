# -*- coding:utf-8  -*-
# @Time     : 2020-7-5 15:53
# @Author   : BGLB
# @Software : PyCharm

from django import template

from comments.models import Comments

register = template.Library()


@register.simple_tag
def parse_commenttree(commentlist, comment):
    """获得当前评论子评论的列表
        用法: {% parse_commenttree article_comments comment as childcomments %}
    """
    datas = []

    def parse(c):
        childs = commentlist.filter(parent_comment=c, is_enable=True)
        for child in childs:
            datas.append(child)
            parse(child)

    parse(comment)
    return datas


@register.simple_tag
def query(qs, **kwargs):
    """ template tag which allows queryset filtering. Usage:
          {% query books author=author as mybooks %}
          {% for book in mybooks %}
            ...
          {% endfor %}
    """
    return qs.filter(**kwargs)


@register.simple_tag
def comment_blog_count(blog_id):
    try:
        count = Comments.objects.filter(blog_id=blog_id).count()
    except Exception as e:
        count = 0
    return count


@register.simple_tag
def comment_user_count(author_id):
    try:
        count = Comments.objects.filter(blog__author_id=author_id).count()
    except Exception as e:
        count = 0
    return count
