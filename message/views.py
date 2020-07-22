from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render


@login_required()
def show_message(request):
    """展示消息列表"""

    user = request.user

    msg_unread = user.notifications.unread()

    msg_read = user.notifications.read()

    return render(request, 'message/message.html', locals())


@login_required()
def update_message(request):
    msg_id = request.GET.get('msg_id')
    if request.method == "GET":
        if msg_id:
            article = request.GET.get('article_id')
            comment = request.GET.get('comment_id')
            msg = request.user.notifications.get(id=msg_id)
            msg.mark_as_read()
            return redirect("/blog/blog-detail/{0}#div-comment-{1}".format(int(article), comment), )
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('message:message-list')
    else:
        msg_id = request.POST.get('msg_id')
        if msg_id:
            request.user.notifications.get(id=msg_id).delete()
        else:
            request.user.notifications.all().delete()
        return JsonResponse({"flag": True, "msg": "删除成功！"})
