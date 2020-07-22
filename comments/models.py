from django.contrib.auth.models import User
from django.db import models
from blog.models import BlogPost
from django.utils.timezone import now


# Create your models here.
class Comments(models.Model):
    content = models.TextField('正文', max_length=300)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)
    owner = models.ForeignKey(User, verbose_name='评论人', on_delete=models.CASCADE)
    blog = models.ForeignKey(BlogPost, verbose_name='文章', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', verbose_name="上级评论", blank=True, null=True, on_delete=models.CASCADE)
    is_enable = models.BooleanField('是否显示', default=True, blank=False, null=False)

    class Meta:
        ordering = ['id']
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        get_latest_by = 'id'

    def __str__(self):
        return self.content
