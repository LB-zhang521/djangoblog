"""bglb_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import notifications.urls
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from bglb_blog import settings
from blog.views import blog_list



urlpatterns = [
    path('admin/admin', admin.site.urls),
  
    path('', blog_list, name='home'),
    path('accounts/', include(('users.urls', 'users'), namespace='accounts')),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('oauth/', include(('oauth.urls', 'oauth'), namespace='oauth')),
    path('notifications/', include(notifications.urls, namespace='notifications')),
    path('comment/', include('comments.urls', namespace='comment')),
    path('message/', include('message.urls', namespace='message')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
