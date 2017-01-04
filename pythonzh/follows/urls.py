from django.conf.urls import url

from . import views

app_name = 'follows'
urlpatterns = [
    url(r'^follow_all/(?P<content_type_id>[^/]+)/(?P<object_id>[^/]+)/(?P<ftype>[a-zA-Z]+)/$',
        views.follow_unfollow, {'actor_only': False}, name='follow_all'),
    url(r'^unfollow_all/(?P<content_type_id>[^/]+)/(?P<object_id>[^/]+)/(?P<ftype>[a-zA-Z]+)/$',
        views.follow_unfollow, {'actor_only': False, 'do_follow': False}, name='unfollow_all'),
]
