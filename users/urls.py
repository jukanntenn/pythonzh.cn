from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url(r'^profile/$', views.UserProfileView.as_view(), name='profile'),
    url(r'^favorites/$', views.UserFavoriteView.as_view(), name='favorite'),
    url(r'^feeds/$', views.UserFeedView.as_view(), name='feed'),
    url(r'^profile/change/$', views.UserProfileChangeView.as_view(), name='profile_change'),
    url(r'^mugshot/change/$', views.MugshotChangeView.as_view(), name='mugshot_change'),
    url(r'^(?P<username>[\w.@+-]+)/$', views.UserDetailView.as_view(), name='detail'),
    url(r'^(?P<username>[\w.@+-]+)/posts/$', views.UserPostListView.as_view(), name='posts'),
    url(r'^(?P<username>[\w.@+-]+)/replies/$', views.UserReplyListView.as_view(), name='replies'),
    url(r'^(?P<username>[\w.@+-]+)/watch/$', views.UserWatchView.as_view(), name='watch'),
    url(r'^(?P<username>[\w.@+-]+)/actions/$', views.UserActionView.as_view(), name='actions'),
    url(r'^(?P<username>[\w.@+-]+)/follows/$', views.UserFollowView.as_view(), name='follows'),
    url(r'^(?P<username>[\w.@+-]+)/praise/$', views.UserPraiseView.as_view(), name='praise'),
]
