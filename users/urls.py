from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url(r'^profile/$', views.UserProfileView.as_view(), name='profile'),
    url(r'^profile/change/$', views.UserProfileChangeView.as_view(), name='profile_change'),
    url(r'^mugshot/change/$', views.MugshotChangeView.as_view(), name='mugshot_change'),
    url(r'^(?P<username>[\w.@+-]+)/$', views.UserDetailView.as_view(), name='detail'),
    url(r'^(?P<username>[\w.@+-]+)/posts/$', views.UserPostListView.as_view(), name='posts'),
    url(r'^(?P<username>[\w.@+-]+)/replies/$', views.UserReplyListView.as_view(), name='replies'),
]
