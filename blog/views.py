# -*- coding:utf-8  -*-
# @Time     : 2020-6-10 11:45
# @Author   : BGLB
# @Software : PyCharm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.datetime_safe import datetime
from notifications.signals import notify
from blog.models import BlogPost, Tag
from django.db.models import Q
from django.core.paginator import Paginator
from blog.utils import update_img_file, blog_tag, blog_category
from comments.models import Comments
from django.utils.timezone import now

def blog_list(request):
    """博客列表页"""
    blog_list = BlogPost.objects.filter(statu='公开').all()
    blog_type = request.GET.get("blog_type", None)
    category = request.GET.get('category', None)
    search = request.GET.get('search', None)
    page = request.GET.get('page')
    if blog_type:
        blog_list = blog_list.filter(blog_type=blog_type).all()
    if category:
        blog_list = blog_list.filter(category=category).all()
    if search:
        blog_list = blog_list.filter(Q(title__icontains=search) | Q(content__icontains=search)|Q(category__name__icontains=search)|
            Q(tag__name=search)).distinct()
    else:
        search = ''
    paginator = Paginator(blog_list, 5)
    blog_list = paginator.get_page(page)
    return render(request, "blog/blog_list.html", locals())


@login_required()
def blog_edit(request):
    """编辑博客"""
    id = request.GET.get('id', None)
    if id is None:  # 新增请求 编辑上次保存的
        blog = BlogPost.objects.filter(author_id=request.user.id, statu='正在编辑').first()
        return render(request, "blog/blog_edit.html", locals())
    else:
        try:
            blog = BlogPost.objects.get(id=id, author_id=request.user.id)
            return render(request, 'blog/blog_edit.html', locals())
        except ObjectDoesNotExist as e:
            return render(request, '404.html', status=403)


def blog_author(request, username):
    user = get_object_or_404(User, username=username)
    blog_all = BlogPost.objects.filter(author_id=user.id).all()
    blog_tag = Tag.objects.filter(blogpost__author_id=user.id)
    blog_list = blog_all.filter(statu='公开')
    if request.user.username == username:
        blog_list_private = blog_all.filter(statu='私密')
        blog_list_del = blog_all.filter(statu="回收站")
        blog_list_drafts = blog_all.filter(statu='草稿箱')
    if blog_all:
        return render(request, 'blog/blog_author.html', locals())
    else:
        return render(request, 'blog/blog_author.html', {"msg": "期待您的创作"})


@login_required()
def blog_delete(request):
    blog_id = request.POST.get('id', None)
    if blog_id:
        blog = get_object_or_404(BlogPost, id=blog_id, author=request.user)

        if blog.statu == "回收站":
            blog.delete()
            msg = "文章已删除"
        else:
            blog.statu = "回收站"
            blog.modify_time = blog.modify_time
            msg = "文章已放入回收站"
            blog.save()
        flag = True

        return JsonResponse({"flag": flag, "msg": msg})

    else:
        return render(request, '404.html',status=404)


def blog_click(request):
    flag = False
    if request.method == "POST":

        blog_id = request.POST.get('id')
        blog = get_object_or_404(BlogPost, id=blog_id)
        blog.like = blog.like+1
        blog.modify_time = blog.modify_time
        blog.save()
        flag = True
        if request.user.is_authenticated:
            if request.user.id != blog.author.id:
                notify.send(request.user, recipient=blog.author, target=blog,
                            verb='给您的博文《{}》点赞啦'.format(blog.title))
        else:
            notify.send(User.objects.filter(is_superuser=True).first(), recipient=blog.author, target=blog,
                        verb='一位陌生人给您的博文《{}》点赞啦'.format(blog.title))

    return JsonResponse({"flag": flag})


def blog_detail(request, id):
    """文章预览和详情页"""
    blog = get_object_or_404(BlogPost, id=id)
    blog_comments = Comments.objects.filter(blog_id=id)
    if blog.statu != '公开' and blog.author != request.user:
        # 非公开的文章并且请求者不是作者 跳转404
        return render(request, '404.html', status=404)
    else:
        blog.click_nums += 1
        blog.modify_time = blog.modify_time
        blog.save()
        return render(request, 'blog/blog_detail.html', locals())


def blog_image(request):
    """上传图片"""
    if request.method == "POST":
        if 'editormd-image-file' in request.FILES:
            img = request.FILES.get('editormd-image-file')
            img_url = update_img_file(img)
            context = {"success": 0, "message": "服务器配置错误，请联系网站管理员进行修复！", 'url': -1}
            if img_url:
                context['success'] = 1
                context['url'] = img_url
            return JsonResponse(context)
    else:
        # get 请求跳转到404
        return render(request, '404.html',status=403)


@login_required()
def blog_publish(request):
    """
    保存博客
    :param request:
    :return:
    """
    if request.method == "POST":
        data = request.POST
        content = data.get("content")
        # 保存文章数据到数据库
        id = data.get('id', 0)
        if id != 0:
            blog = BlogPost.objects.filter(author_id=request.user.id, id=id)
        else:
            blog = BlogPost.objects.filter(author_id=request.user.id, statu='正在编辑')
        if blog.exists():
            blog = blog.first()
            blog.tag.clear()

        else:
            blog = BlogPost()
        blog.content = content
        blog.statu = data.get("statu")
        blog.author = User.objects.get(id=request.user.id)
        blog.category_id = data.get("category")
        blog.blog_type = data.get("type")
        blog.title = data.get('title')
        tag_list = []
        blog.modify_time = now()
        blog.save()
        if data.get("tag_add"):
            tag_add = blog_tag(data.get("tag_add"))
            # print(data.get("tag_add"))
            tag_list = tag_add
        if data.get('tag'):
            for tag in data.get('tag').split(','):
                tag_list.append(tag)
        # print(tag_list)
        if len(tag_list) > 0:
            tag_list = list(set(tag_list))
            if '' in tag_list:
                tag_list.remove('')
            blog.tag.add(*tag_list)

        context = {"flag": True, "message": "博文发布成功！", 'id': blog.id}
        return JsonResponse(context)
    else:
        context = {"categorys": blog_category(), 'tags': blog_tag()}
        return JsonResponse(context)

