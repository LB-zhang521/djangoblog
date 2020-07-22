from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here
from comments.utils import send_notification
from .models import Comments


@login_required()
def comment_save(request):
    """提交评论"""
    if request.method == "GET":
        return render(request, '404.html')
    owner = request.user
    data = request.POST
    content = data.get('content')
    blog_id = data.get('blog_id')
    parent_id = data.get('parent_comment_id')
    comment = Comments.objects.create(owner=owner, content=content, blog_id=blog_id)
    if parent_id is not '0':
        parent_comment = Comments.objects.get(pk=parent_id)
        comment.parent_comment = parent_comment
    comment.save()
    flag = True
    msg = "评论成功"
    send_notification(comment)
    return JsonResponse({'flag': flag, 'msg': msg})


@login_required()
def comment_delete(request):
    """删除评论"""
    if request.method == "GET":
        return render(request, '404.html')
    try:
        comment = Comments.objects.get(id=request.POST.get('id'))
        comment.delete()
        flag = True
        msg = "删除成功"
    except Exception as e:
        flag = False
        msg = "数据错误"
    return JsonResponse({'flag': flag, 'msg': msg})
