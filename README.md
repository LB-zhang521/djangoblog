# bglb_blog

本项目是基于`python3.6`和`Django2.2`的多人博客

## 主要功能：
- 登录，注册，邮箱验证，注册的用户也可以发布文章
- 文章，分类目录，标签的添加，删除，编辑等。
- 支持公告，广告，友情链接-（后台增加）
- 文章支持`Markdown`，支持代码高亮- 基于Editor.md
- 支持简单的全站搜索，基于Q查询
- 支持评论功能，包括发表回复评论，以及评论的站内提醒
- 支持第三方，QQ登录，github登录
- 简单的SEO功能，新建文章等会自动推送百度
- 集成了简单的阿里云图床功能
- 基于`boostarp4` 适配手机端

## 项目部分截图

![首页](https://blog.bglb.work/img/image-20200722172712277.png?x-oss-process=style/blog_img)



![博主主页](https://blog.bglb.work/img/1595410458768.png?x-oss-process=style/blog_img)



![文章详情页](https://blog.bglb.work/img/1595410549486.png?x-oss-process=style/blog_img)



![用户信息](https://blog.bglb.work/img/1595410713670.png?x-oss-process=style/blog_img)



![后台管理](https://blog.bglb.work/img/1595410611312.png?x-oss-process=style/blog_img)





## 运行测试

 1. 下载项目到本地
 2. 下载环境依赖

```shell
pip install -r requirements.txt

```

3. 同步数据库
```shell
python manage.py makemigrations
python manage.py migrate

```

4. 创建管理员账户并启动项目
 ```bash
 # 创建管理员
 python manage.py createsuperuser
 # 启动项目
 python manage.py runserver
 ```

5. 打开浏览器，进入后台
后台地址 ：`127.0.0.1:8000/admin`
首页地址 ：`127.0.0.1:8000`

**ps1：创建的管理员没有头像以及其他用户信息，因为管理员不会参与发布文章之类的，若想要管理员更普通用户一样，需要在后台添加管理员的基本信息**

![图片alt](https://blog.bglb.work/img/1595410837081.png?x-oss-process=style/blog_img)

**ps2：注册新用户之前，需要配置邮件功能，这部分在setting.py中，自行配置**

**ps3：图床功能，使用了阿里云的oss对象存储，需要在`blog/utils.py`里面配置相关的oss ID 以及key**

**ps4：第三方登录，需要在后台配置相关的appkey以及appsecret**

现在已经支持QQ，GitHub，需要在其对应的开放平台申请oauth登录权限，然后在 

**后台->Oauth** 配置中新增配置，填写对应的`appkey`和`appsecret`以及回调地址。  

**回调地址：**

- qq：http://你的域名/oauth/authorize?type=qq
- github：http://域名/oauth/oauthorize?type=github

## 声明

- 本项目参考了 [liangliangyy](https://github.com/liangliangyy/DjangoBlog) 和 [杜赛](https://github.com/stacklens/django_blog_tutorial/tree/master/md) 两位大佬的博客项目，感谢两位大佬的源码贡献以及文档详解
- 此本项只用于交流学习，如果您用于其他用途，责任自负；若有侵权，请通过bglb@qq.com邮箱联系我



另外： 欢迎大家访问我的博客[蓝白社区](https://blog.bglb.work)，有什么问题也可以直接加入交流群或者直接通过邮箱联系我

