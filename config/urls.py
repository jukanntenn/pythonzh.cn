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
from django.contrib.sitemaps.views import sitemap

from forum.views import follow_unfollow
from forum.feeds import AllPostsRssFeed, AllPostsAtomFeed
from forum.sitemaps import sitemaps

urlpatterns = [
    # Follow/Unfollow API
    url(r'^activity/follow/(?P<content_type_id>[^/]+)/(?P<object_id>[^/]+)/(?:(?P<follow_type>[^/]+)/)?$',
        follow_unfollow, {'send_action': False}, name='actstream_follow'),
    url('', include('forum.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^user/', include('users.urls')),
    url(r'^user/', include('allauth.urls')),
    url(r'^notifications/', include('notifications.urls', namespace='notifications')),
    url(r'^replies/', include('django_comments.urls')),
    url(r'^replies/', include('replies.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^activity/', include('actstream.urls')),
    url(r'^all/rss/$', AllPostsRssFeed()),
    url(r'^all/atom/$', AllPostsAtomFeed()),
    url(r'^robots\.txt', include('robots.urls')),
    url(r'^sitemap\.xml$', sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
