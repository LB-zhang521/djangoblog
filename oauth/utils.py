# -*- coding:utf-8  -*-
# @Time     : 2020-7-5 14:35
# @Author   : BGLB
# @Software : PyCharm


from abc import ABCMeta, abstractmethod
from io import BytesIO
from threading import Thread
from urllib import parse
from urllib.request import urlopen

from django.core.files import File

from users.models import UsersProfile
from .models import OAuthUser, OAuthConfig

import requests
import json

import urllib


class OAuthAccessTokenException(Exception):
    '''
    oauth授权失败异常
    '''


class BaseOauthManager(metaclass=ABCMeta):
    """获取用户授权"""
    AUTH_URL = None
    """获取token"""
    TOKEN_URL = None
    """获取用户信息"""
    API_URL = None
    '''icon图标名'''
    ICON_NAME = None

    def __init__(self, access_token=None, openid=None):
        self.access_token = access_token
        self.openid = openid

    @property
    def is_access_token_set(self):
        return self.access_token is not None

    @property
    def is_authorized(self):
        return self.is_access_token_set and self.access_token is not None and self.openid is not None

    @abstractmethod
    def get_authorization_url(self, nexturl='/'):
        pass

    @abstractmethod
    def get_access_token_by_code(self, code):
        pass

    @abstractmethod
    def get_oauth_userinfo(self):
        pass

    def do_get(self, url, params, headers=None):
        rsp = requests.get(url=url, params=params, headers=headers)
        # logger.info(rsp.text)
        return rsp.text

    def do_post(self, url, params, headers=None):
        rsp = requests.post(url, params, headers=headers)
        # logger.info(rsp.text)
        return rsp.text

    def get_config(self):
        value = OAuthConfig.objects.filter(oauth_type=self.ICON_NAME)
        return value[0] if value else None


class GitHubOauthManager(BaseOauthManager):
    AUTH_URL = 'https://github.com/login/oauth/authorize'
    TOKEN_URL = 'https://github.com/login/oauth/access_token'
    API_URL = 'https://api.github.com/user'
    ICON_NAME = 'github'

    def __init__(self, access_token=None, openid=None):
        config = self.get_config()
        self.client_id = config.appkey if config else ''
        self.client_secret = config.appsecret if config else ''
        self.callback_url = config.callback_url if config else ''
        super(
            GitHubOauthManager,
            self).__init__(
            access_token=access_token,
            openid=openid)

    def get_authorization_url(self, nexturl='/'):
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.callback_url+'&next_url='+nexturl,
            'scope': 'user'
        }
        url = self.AUTH_URL+"?"+urllib.parse.urlencode(params)
        return url

    def get_access_token_by_code(self, code):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': code,

            'redirect_uri': self.callback_url
        }
        rsp = self.do_post(self.TOKEN_URL, params)

        r = parse.parse_qs(rsp)
        if 'access_token' in r:
            self.access_token = (r['access_token'][0])
            return self.access_token
        else:
            raise OAuthAccessTokenException(rsp)

    def get_oauth_userinfo(self):

        rsp = self.do_get(self.API_URL, params={}, headers={
            "Authorization": "token "+self.access_token
        })

        datas = json.loads(rsp)
        # {"login": "LB-zhang521", "id": 54814510, "node_id": "MDQ6VXNlcjU0ODE0NTEw",
        #  "avatar_url": "https://avatars1.githubusercontent.com/u/54814510?v=4", "gravatar_id": "",
        #  "url": "https://api.github.com/users/LB-zhang521", "html_url": "https://github.com/LB-zhang521",
        #  "followers_url": "https://api.github.com/users/LB-zhang521/followers",
        #  "following_url": "https://api.github.com/users/LB-zhang521/following{/other_user}",
        #  "gists_url": "https://api.github.com/users/LB-zhang521/gists{/gist_id}",
        #  "starred_url": "https://api.github.com/users/LB-zhang521/starred{/owner}{/repo}",
        #  "subscriptions_url": "https://api.github.com/users/LB-zhang521/subscriptions",
        #  "organizations_url": "https://api.github.com/users/LB-zhang521/orgs",
        try:
            oauth_user = OAuthUser()
            oauth_user.openid = datas.get('id', None)
            oauth_user.type = 'github'
            oauth_user.token = self.access_token
            oauth_user.userdata = rsp
            user_pro = UsersProfile()
            #temp = save_avatar(datas.get('avatar_url','github'+str(oauth_user.openid)))
            #if temp:
            #    user_pro.avatar = temp
            # else:
            #     user_pro.avatar = None
            user_pro.nikename = datas.get('name', None)
            user_pro.github = datas.get('html_url', None)
            user_pro.site = datas.get('blog', '')
            return oauth_user, user_pro
        except Exception as e:
            print('获取用户信息错误：', e)
            return None
        # logger.error(e)
        # logger.error('github oauth error.rsp:'+rsp)


class QQOauthManager(BaseOauthManager):
    AUTH_URL = 'https://graph.qq.com/oauth2.0/authorize'
    TOKEN_URL = 'https://graph.qq.com/oauth2.0/token'
    API_URL = 'https://graph.qq.com/user/get_user_info'
    OPEN_ID_URL = 'https://graph.qq.com/oauth2.0/me'
    ICON_NAME = 'qq'

    def __init__(self, access_token=None, openid=None):
        config = self.get_config()
        self.client_id = config.appkey if config else ''
        self.client_secret = config.appsecret if config else ''
        self.callback_url = config.callback_url if config else ''
        super(
            QQOauthManager,
            self).__init__(
            access_token=access_token,
            openid=openid)

    def get_authorization_url(self, nexturl='/'):
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.callback_url+'&next_url='+nexturl,
        }
        url = self.AUTH_URL+"?"+urllib.parse.urlencode(params)
        return url

    def get_access_token_by_code(self, code):
        params = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.callback_url
        }
        rsp = self.do_get(self.TOKEN_URL, params)
        if rsp:
            d = urllib.parse.parse_qs(rsp)
            if 'access_token' in d:
                token = d['access_token']
                self.access_token = token
                return token
        else:
            raise OAuthAccessTokenException(rsp)

    def get_open_id(self):
        if self.is_access_token_set:
            params = {
                'access_token': self.access_token
            }
            rsp = self.do_get(self.OPEN_ID_URL, params)
            if rsp:
                rsp = rsp.replace(
                    'callback(', '').replace(
                    ')', '').replace(
                    ';', '')
                obj = json.loads(rsp)
                openid = str(obj['openid'])
                self.openid = openid
                return openid

    def get_oauth_userinfo(self):
        openid = self.get_open_id()
        if openid:
            params = {
                'access_token': self.access_token,
                'oauth_consumer_key': self.client_id,
                'openid': self.openid
            }
            rsp = self.do_get(self.API_URL, params)
            # logger.info(rsp)
            datas = json.loads(rsp)
            oauth_user = OAuthUser()
            oauth_user.openid = openid
            oauth_user.type = 'qq'
            oauth_user.token = self.access_token
            oauth_user.userdata = rsp
            user_pro = UsersProfile()
           # temp = save_avatar(datas.get('avatar_url'), 'qq'+str(oauth_user.openid))
           # if temp:
           #     user_pro.avatar = temp
           # else:
           #     user_pro.avatar = None
            user_pro.nikename = datas.get('nickname', None)
            user_pro.gender = datas.get('gender', '男')
            return oauth_user, user_pro


def get_oauth_apps():
    configs = OAuthConfig.objects.filter(is_enable=True).all()
    if not configs:
        return []
    configtypes = [x.oauth_type for x in configs]
    applications = BaseOauthManager.__subclasses__()
    apps = [x() for x in applications if x().ICON_NAME.lower() in configtypes]
    return apps


def get_manager_by_type(_type):
    applications = get_oauth_apps()
    if applications:
        finds = list(
            filter(
                lambda x: x.ICON_NAME.lower() == _type.lower(),
                applications))
        if finds:
            return finds[0]
    return None


def async_my(f):
    """
    异步下载
    :param f:
    :return:
    """

    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


@async_my
def save_avatar(url, img_name):
    try:
        r = urlopen(url)
        io = BytesIO(r.read())
        img = ("{}.jpg".format(img_name), File(io))
    except Exception as e:
        print(e)
        img = None
    return img
