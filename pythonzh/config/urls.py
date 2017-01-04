"""djangozh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

from users import views
from forum.feeds import AllPostsRssFeed, AllPostsAtomFeed

urlpatterns = [
    url('', include('forum.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include('allauth.account.urls')),
    url(r'^follows/', include('follows.urls')),
    url(r'^notifications/', include('notifications.urls', namespace='notifications')),
    url(r'^replies/', include('django_comments.urls')),
    url(r'^replies/', include('replies.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^category/', include('categories.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^all/rss/$', AllPostsRssFeed()),
    url(r'^all/atom/$', AllPostsAtomFeed()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
