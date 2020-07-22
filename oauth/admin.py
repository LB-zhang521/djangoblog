from django.contrib import admin
# Register your models here.
from .models import OAuthUser, OAuthConfig
from django.urls import reverse
from django.utils.html import format_html
import logging


# logger = logging.getLogger(__name__)


class OAuthConfigAdmin(admin.ModelAdmin):
    list_display = ('oauth_type', 'appkey', 'appsecret', 'is_enable')
    list_filter = ('oauth_type',)


class OAuthUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'openid', 'token', 'type', 'created_time', 'last_mod_time')


admin.site.register(OAuthUser, OAuthUserAdmin)
admin.site.register(OAuthConfig, OAuthConfigAdmin)
