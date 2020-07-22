# -*- coding:utf-8  -*-
# @Time     : 2020-7-4 12:40
# @Author   : BGLB
# @Software : PyCharm
"""
辅助函数

"""

import random
import base64

from django.contrib.auth.models import User
from django.core.mail import send_mail
from bglb_blog.settings import DEFAULT_FROM_EMAIL, DOMAIN, SECRET_KEY
from itsdangerous import URLSafeTimedSerializer as utsr


class Token:
    """token类"""

    def __init__(self, security_key=SECRET_KEY):
        self.security_key = security_key
        self.salt = base64.encodebytes(security_key.encode('utf8'))

    # 生成token
    def generate_validate_token(self, userdata):
        serializer = utsr(self.security_key)
        return serializer.dumps(userdata, self.salt)

    # 验证token
    def confirm_validate_token(self, token, expiration=3600):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)

    # 移除token
    def remove_validate_token(self, token):
        serializer = utsr(self.security_key)
        # print(serializer.loads(token, salt=self.salt))
        return serializer.loads(token, salt=self.salt)


def activate_mail(email, email_type, email_content):
    """
    :param email: 用户地址
    :param email_type: 邮件类型
    :param email_content: 邮件内容
    :return: 发送结果
    """
    context = {"flag": False, "msg": "网络异常！！！稍后重试"}
    user = User.objects.filter(email=email)
    if not user.exists():
        context["msg"] = "您未注册，请前往注册"
        return context
    user = user.first()
    username = user.username

    email_title = '半根蓝白博客站点-{}邮件'.format(email_type)
    email_body = \
        """
            <div style="background-color:#ECECEC; padding: 35px;">
                <table cellpadding="0" align="center"style="width: 600px; margin: 0px auto; text-align: left; position: relative; border-top-left-radius: 5px; border-top-right-radius: 5px; border-bottom-right-radius: 5px; border-bottom-left-radius: 5px; font-size: 14px; font-family:微软雅黑, 黑体; line-height: 1.5; box-shadow: rgb(153, 153, 153) 0px 0px 5px; border-collapse: collapse; background-position: initial initial; background-repeat: initial initial;background:#fff;">
                <tbody>
                    <tr><th valign="middle"style="height: 25px; line-height: 25px; padding: 15px 35px; border-bottom-width: 1px; border-bottom-style: solid; border-bottom-color: #42a3d3; background-color: #49bcff; border-top-left-radius: 5px; border-top-right-radius: 5px; border-bottom-right-radius: 0px; border-bottom-left-radius: 0px;">
                    <a href='{host}'>
                        <img src='http://www.bglb.work/img/logos/logo_font.png' alt='站点LOGO'>
                    </a>
                    <font face="微软雅黑" size="5" style="color: rgb(255, 255, 255); ">半根蓝白博客站点{email_type}</font>
                    </th></tr><tr><td>
                    <div style="padding:25px 35px 40px; background-color:#fff;">
                    <h2 style="margin: 5px 0px; ">
                        <font color="#333333" style="line-height: 20px; ">
                        <font style="line-height: 22px; " size="4">亲爱的 {email}：</font></font></h2>
                    <p>感谢您注册本站点！下面是您的账号信息，以及操作提示<br>您的用户ID：<b>{userId}</b><br>{content}</p>
                    <p align="right">如果您未注册本站点，请与本站取得联系<br>回复地址：bglb@qq.com</p>
                    <div style="width:700px;margin:0 auto;">
                    <div style="padding:10px 10px 0;border-top:1px solid #ccc;color:#747474;margin-bottom:20px;line-height:1.3em;font-size:12px;"><p>此为系统邮件，请勿回复<br>请保管好您的邮箱，避免账号被他人盗用<br>给您造成的困扰，本站感到万分抱歉</p>
                    </div></div></div></td></tr>
                </tbody>
                </table>
            </div>      
        """.format(host=DOMAIN, email=email, userId=username, email_type=email_type, content=email_content)

    send_status = send_mail(email_title, "", DEFAULT_FROM_EMAIL, [email], html_message=email_body)
    if send_status:
        context["flag"] = True
        context["msg"] = "请前往您的注册邮箱中查看邮件"
    else:
        context["flag"] = False
        context["msg"] = "邮件发送失败，请稍后重试"
    return context


# send_mail(
# subject,邮件标题
# message,邮件内容
# from_email,发件人
# recipient_list,[收件人列表]
# fail_silently=False, 是否报错
# auth_user=None, 发件的服务器用户名
# auth_password=None,发件的服务器密码
# connection=None, 表示这个的链接对象
# html_message=None html类型
# )


def active_yzm(len=6):
    """生成六位验证码"""
    tmp_list = []
    for i in range(len):
        u = chr(random.randint(65, 90))  # 生成大写字母
        l = chr(random.randint(97, 122))  # 生成小写字母
        n = str(random.randint(0, 9))
        tmp = random.choice([u, l, n])
        tmp_list.append(tmp)

    return "".join(tmp_list)
