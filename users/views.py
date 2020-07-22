# -*- coding:utf-8  -*-
# @Time     : 2020-6-10 11:45
# @Author   : BGLB
# @Software : PyCharm

from django.http import JsonResponse
from notifications.signals import notify
from pytz import unicode
from users.utils import Token, activate_mail, active_yzm
from .models import UsersProfile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from bglb_blog.settings import DOMAIN
from django.shortcuts import HttpResponse

token_confirm = Token()


def user_login(request):
    """用户登录"""
    if request.method == 'POST':
        context = {"flag": False, "msg": "用户名或密码错误"}
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        if "@" in username:
            user = User.objects.filter(email=username).first()
        else:
            user = User.objects.filter(username=username).first()
        if user:
            if user.is_active:
                user = authenticate(username=user.username, password=password)
                if user:
                    login(request, user)
                    context['flag'] = True
                    context['msg'] = '登录成功'
            else:
                token = token_confirm.generate_validate_token(userdata=user.username)
                token_url = '/'.join([DOMAIN, 'accounts/activate', token])
                email_content = \
                    """
                    确认无误后，请在<span style='color:red;'>一小时之内</span>点击<a style='color:blue' href='{token_url}'>链接</a>激活邮箱<br>
                    若无法跳转，请直接在浏览器打开此链接：<br><b style='color:blue'>{token_url}</b>
                    """.format(
                        token_url=token_url)
                _type = "注册"
                activate_mail(user.email, _type, email_content)
                context["msg"] = "您的邮箱未激活，请前往{}邮箱查看激活邮件".format(user.email)

        return JsonResponse(context)
    else:
        if request.user.is_authenticated:
            return redirect('blog:blog_list')
        else:
            return render(request, "accounts/login.html")


def user_logout(request):
    """用户退出"""
    logout(request)
    return redirect("accounts:login")


def user_reg(request):
    """用户注册"""
    if request.method == 'POST':
        context = {"flag": False, "msg": ""}
        data = request.POST
        user = User.objects.filter(username=data.get('username')).first()  # 判断用户名是否存在
        if not user:
            user = User.objects.filter(email=data.get('email')).first()  # 判断email 邮箱是否存在
            if not user:
                new_user = User.objects.create(username=data.get('username'), email=data.get('email'))
                new_user.set_password(data.get('password'))

                new_user.is_active = False
                new_user.save()

                user_profile_user = User.objects.get(username=data.get('username')).id
                user_data = UsersProfile()
                user_data.user_id = user_profile_user
                user_data.save()

                context['flag'] = True
                context['msg'] = "注册成功，需要激活邮箱"

                return JsonResponse(context)
            else:
                context["msg"] = "邮箱已经被绑定别的用户名，如果这是您的邮箱，请直接登录！！！"
                return JsonResponse(context)
        else:
            context["msg"] = "您来晚了一步，用户名已经被注册"
            return JsonResponse(context)
    else:
        return render(request, 'accounts/reg.html')


@login_required(login_url='accounts/login')
def update_email(request):
    flag = False
    msg = "未知错误"
    if request.method == "POST":
        email = request.POST.get("new_email")
        yzm = request.POST.get("yzm")
        user = User.objects.get(user_id=request.user.user_id)
        if yzm.upper() == request.session.get("email_yzm").upper():
            if User.objects.filter(email=email).exists():
                flag = False
                msg = "该邮箱已经绑定其他用户名，请重新绑定，重新获取验证码"
            else:
                user.email = email
                user.is_active = False
                user.save()
                flag = True
                msg = "邮箱更改成功，请重新登录"
                user_logout(request)
        else:
            flag = False
            msg = "验证码错误，请重新获取验证码"
        yzm = request.session.pop("email_yzm", None)
        print(yzm+"更改邮箱的验证码已经删除")
    return JsonResponse({"flag": flag, "msg": msg})


@login_required(login_url='accounts/login')
def update_password(request):
    """修改密码"""
    if request.method == "POST":
        print(request.POST)
        new_password = request.POST.get("new_password")
        user_cur = User.objects.get(user_id=request.user.user_id)
        user_cur.set_password(new_password)
        user_cur.save()
        _type = "修改密码通知"
        email_content = \
            """
            您<span style="color:red;">修改密码</span><br>
            修改密码成功
            若不是您本人操作，请尽快联系本站点
            """
        activate_mail(user_cur.email, _type, email_content)
        logout(request)
        return redirect("accounts:login")


def reset_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get("password")
        yzm = request.POST.get("yzm")
        print(request.POST)
        if yzm.upper() == request.session.get("password_reset").upper():
            user_cur = User.objects.get(email=email)

            user_cur.set_password(password)
            user_cur.save()
            flag = True
            msg = "密码重置成功，请登录"
            _type = "重置密码通知"
            email_content = \
                """
                您刚才<span style="color:red;">重置密码</span><br>
                密码重置成功<br>
                若不是您本人操作，请尽快联系本站点
                """
            activate_mail(user_cur.email, _type, email_content)
        else:
            flag = False
            msg = "验证码错误，请重新获取验证码"
        yzm = request.session.pop("password_reset", None)
        return JsonResponse({"flag": flag, "msg": msg})


def email_result(request):
    if request.method == "POST":
        email_type = request.POST.get("email_type")
        if email_type == "reg":
            email = request.POST.get("email")
            token = token_confirm.generate_validate_token(userdata=email)
            token_url = '/'.join([DOMAIN, 'accounts/activate', token])
            email_content = \
                """
                确认无误后，请在<span style='color:red;'>一小时之内</span>点击<a style='color:blue' href='{token_url}'>链接</a>激活邮箱<br>
                若无法跳转，请直接在浏览器打开此链接：<br><b style='color:blue'>{token_url}</b>
                """.format(
                    token_url=token_url)
            _type = "注册"

        elif email_type == "email_change":
            _type = "更改邮箱"
            email = request.user.email
            yzm = active_yzm()
            request.session["email_yzm"] = yzm
            email_content = \
                """
                您正在<span style="color:red;">更改邮箱地址</span><br>
                您本次操作的验证码:<b>{yzm}</b><br>
                若不是您本人操作，请尽快更改密码
                """.format(yzm=yzm)
        elif email_type == "password_reset":
            _type = "重置密码"
            email = request.POST.get('email')
            yzm = active_yzm()
            request.session["password_reset"] = yzm
            email_content = \
                """
                您正在尝试<span style="color:red;">重置密码</span><br>
                您本次操作的验证码：<b>{yzm}</b><br>
                若不是您本人操作，请尽快更改密码
                """.format(yzm=yzm)
        else:
            return JsonResponse({"error": "未知错误"})
        email_statu = activate_mail(email, _type, email_content)
        notify.send(User.objects.get(email=email), recipient=User.objects.filter(is_superuser=True), target=User.objects.get(email=email),
                    verb='{}用户通过账号操作{}，验证邮件发送结果{}'.format(email, _type, email_statu['flag']))
        return JsonResponse(email_statu)


@login_required(login_url='/accounts/login/')
def profile(request):
    """修改用户信息"""
    profile = UsersProfile.objects.get(user_id=request.user.id)

    if request.method == 'POST':
        data = request.POST
        print(data)
        is_display = data.get('is_display', None)
        if is_display:
            profile.telephone = data.get("telephone")
            profile.qq = data.get("qq")
            profile.github = data.get("github")
            profile.site = data.get("site")
            profile.is_display = is_display
            profile.occupation = data.get('occupation')
        elif 'avatar' in request.FILES:
            request.FILES.get('avatar').name = request.user.username+"."+ \
                                               str(request.FILES.get('avatar').name).split('.')[1]
            profile.avatar.delete()
            profile.avatar = request.FILES.get("avatar")
            print(profile.avatar)
        else:
            profile.gender = data.get("gender")
            profile.nickname = data.get("nickname")
            profile.sign = data.get("sign")
            profile.age = data.get("age")

        profile.save()

        return redirect("accounts:profile")
    else:
        print(profile.avatar)
        return render(request, "accounts/profile.html", locals())


def activate(request, token):
    """ 验证"""
    context = {"flag": False, "msg": '未知错误，请重新注册，或稍后重试！！！'}
    try:
        email = token_confirm.confirm_validate_token(token)
    except:  # 令牌过期
        token_confirm.remove_validate_token(token)
        context["msg"] = '半根蓝白博客站点提示您，验证链接已过期，请重新获取激活邮件'
        context["url"] = unicode(DOMAIN)+u'/accounts/reg'
        return render(request, 'accounts/user_active_result.html', context)
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        context["msg"] = '半根蓝白博客站点提示您，您所验证的用户不存在'
        context["url"] = unicode(DOMAIN)+u'/accounts/reg/'
        return render(request, 'accounts/user_active_result.html', context)

    user.is_active = True
    user.save()
    token_confirm.remove_validate_token(token)  # 移除此用户的token
    context["flag"] = True
    context["msg"] = '半根蓝白博客站点提示您，您的账户激活成功现在可以使用，'
    context["url"] = unicode(DOMAIN)+u'/accounts/profile'
    login(request, user)

    return render(request, 'accounts/user_active_result.html', context)
