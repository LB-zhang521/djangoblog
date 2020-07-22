# -*- coding:utf-8  -*-
# @Time     : 2020-7-11 14:15
# @Author   : BGLB
# @Software : PyCharm
import oss2

from blog.models import Category, Tag
from bglb_blog.settings import DOMAIN

def update_img_file(image):
    """
    ！ 上传单张图片
    :param image: b字节文件
    :return: 若成功返回图片路径，若不成功返回空
    """
    auth = oss2.Auth('AccessKey ID', 'AccessKey')

    bucket = oss2.Bucket(auth, 'bucket外网域名', 'bucket名称')

    base_img_name = "img/"+image.name

    res = bucket.put_object(base_img_name, image)
    # print(base_img_name)
    # print(res)
    image_url = "bucket外网访问域名"+'/img/'+image.name+"?x-oss-process=style/blog_img"
    if res.status == 200:
        result = image_url
        # print(image_url)
    else:
        result = None
    return result


def blog_category():
    """返回文章分类"""
    category = Category.objects.values("id", "name")

    return list(category)


def blog_tag(tags=None):
    if tags:
        new_tag_id = []
        tags_list = str(tags).split(",")
        for tag in tags_list:
            if tag != '':
                if Tag.objects.filter(name=tag).exists():
                    continue
                else:
                    new_tag = Tag.objects.create(name=tag)
                    new_tag.save()
                    new_tag_id.append(Tag.objects.get(name=tag).id)
        print(new_tag_id)
        return new_tag_id
    else:
        blog_tags = Tag.objects.values("id", "name")

        return list(blog_tags)
