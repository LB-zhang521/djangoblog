from notifications.signals import notify

from oauth.utils import get_manager_by_type, OAuthAccessTokenException
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from bglb_blog.settings import DOMAIN
from django.contrib.auth import login

from users.models import UsersProfile
from users.utils import activate_mail
from users.views import token_confirm
from django.http import JsonResponse
from oauth.models import OAuthUser
from urllib.parse import urlparse
import datetime


def get_redirecturl(request):
    """取得跳转url"""
    nexturl = request.GET.get('next_url', None)
    if not nexturl or 'login/' in nexturl:
        nexturl = '/'
        return nexturl
    p = urlparse(nexturl)
    if p.netloc:
        site = DOMAIN
        if not p.netloc.replace('www.', '') == site.replace('www.', ''):
            # logger.info('非法url:'+nexturl)
            return "/"
    return nexturl


def oauthlogin(request):
    """第三方登录的起始"""
    type = request.GET.get('type', None)
    if not type:
        return ('/')
    manager = get_manager_by_type(type)
    if not manager:
        return redirect('/')
    nexturl = get_redirecturl(request)
    # 授权链接
    authorizeurl = manager.get_authorization_url(nexturl)
    return redirect(authorizeurl)


def authorize(request):
    """授权回调成功之后的页面"""
    type = request.GET.get('type', None)
    if not type:
        return redirect('/')
    manager = get_manager_by_type(type)
    if not manager:
        return redirect('/')
    code = request.GET.get('code', None)
    try:
        rsp = manager.get_access_token_by_code(code)
    except OAuthAccessTokenException as e:
       print(e)
       return redirect('/')
    except Exception as e:
        print(e)
        # logger.error(e)
        rsp = None
    nexturl = get_redirecturl(request)
    if not rsp:
        return redirect(manager.get_authorization_url(nexturl))
    oauth_user, user_pro = manager.get_oauth_userinfo()
   
    if oauth_user:
        try:
            oauth_user = OAuthUser.objects.get(type=type, openid=oauth_user.openid)
            user = oauth_user.user
        except ObjectDoesNotExist as e:
            # 写入日志-- 新用户注册通过第三方
            # OAuthUser之前没有这个用户， 用户表创建一个 默认密码 是oauth.type + oauth.openid
            user = User.objects.create()
            user.is_active = False
            user.username = oauth_user.type+datetime.datetime.now().strftime('%I%M%S')
            user.set_password(oauth_user.type+str(oauth_user.openid))
            user.save()
            user_pro.nickname = oauth_user.type+datetime.datetime.now().strftime('%I%M%S')
            user_pro.user = user

            user_pro.save()
            oauth_user.user = user
        userPro = UsersProfile.objects.get(user_id=user.id)
        userPro.save()
        oauth_user.save()

        if user.is_active:
            login(request, user)
            return redirect('blog:blog_list')
            # return redirect('accounts:profile')
        else:
            request.session["oauthid"] = oauth_user.id
            return redirect('oauth:bindemail')
    else:
        return redirect(nexturl)


def bindemail(request):
    """
    绑定邮箱
    :param request:
    :return:
    """
    try:
        oauth = OAuthUser.objects.get(id=request.session.get("oauthid"))
    except ObjectDoesNotExist as e:
       # print((e)
        return render(request,'404.html',status=404)

    if request.method == "GET":
        return render(request, 'oauth/bindemail.html')
    else:
        data = request.POST
        email = data.get('email')
        username = data.get('username')
        if User.objects.filter(username=username).exists():
            flag = False
            msg = '用户名已存在'
            return JsonResponse({'flag': flag, 'msg': msg})
        if User.objects.filter(email=email).exists():
            flag = False
            msg = '邮箱已注册'
            return JsonResponse({'flag': flag, 'msg': msg})
        user = oauth.user
        user.username = username
        user.email = email
        user.save()
        token = token_confirm.generate_validate_token(userdata=email)
        token_url = '/'.join([DOMAIN, 'accounts/activate', token])
        email_content = \
            """
            您刚才通过{oauth_type}快捷注册了本站<br>
            您的默认密码为<span style='color:red;'>{user_password}<b>请务必更改密码！！！</b></span><br />
            确认无误后，请在<span style='color:red;'>一小时之内</span>点击<a style='color:blue' href='{token_url}'>链接</a>激活邮箱<br>
            若无法跳转，请直接在浏览器打开此链接：<br><b style='color:blue'>{token_url}</b>
            """.format(
                token_url=token_url, user_password=oauth.type+oauth.openid, oauth_type=oauth.type, userid=username)
        _type = "注册"

        context = activate_mail(email, _type, email_content)
        notify.send(user, recipient=User.objects.filter(is_superuser=True), target=user, verb='{}用户通过{}操作{}，验证邮件发送结果{}'.format(email, oauth.type, _type, context['flag']))
        return JsonResponse(context)
