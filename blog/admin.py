from django.contrib import admin

# Register your models here.


from blog.models import Category, Tag, BlogPost, Notice, Links, AD


class BlogPostAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('title', 'author', 'blog_type', 'category', 'create_time', 'click_nums', 'like', 'statu')
    list_filter = ('category', 'statu', 'author', 'blog_type',)


class TagAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('id', 'name')


class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('id', 'name')


class LinksAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('id', 'name', 'link', 'is_enable', 'created_time', 'last_mod_time')


class NoticeAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('id', 'title', 'content', 'is_enable', 'created_time', 'last_mod_time')


class ADAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('id', 'title', 'content', 'is_enable', 'created_time', 'last_mod_time')


admin.site.register(Category, CategoryAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(Links, LinksAdmin)
admin.site.register(AD, ADAdmin)

admin.site.site_header = '半根蓝白博客站点'
admin.site.site_title = '蓝白站点后台管理'
admin.site.index_title = '博客后台管理'
