from django.contrib import admin
# Register your models here.
from django.utils.safestring import mark_safe

from users.models import UsersProfile


class UsersProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'avatar_img', 'qq', 'github', 'site')
    list_filter = ('user', 'qq', 'github')

    def avatar_img(self, obj):
        return mark_safe('<img src="{}" height="64" width="64" style="border-radius:50%"/>'.format(obj.avatar.url))

    avatar_img.allow_tags = True


admin.site.register(UsersProfile, UsersProfileAdmin)
