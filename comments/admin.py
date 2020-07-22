from django.contrib import admin

# Register your models here.
from comments.models import Comments


class CommentsAdmin(admin.ModelAdmin):
    list_filter = ['owner', 'blog']
    list_display = ['id', 'owner', 'content', 'created_time', 'last_mod_time', 'blog', 'is_enable']


admin.site.register(Comments, CommentsAdmin)
