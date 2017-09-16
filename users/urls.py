from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url(r'^settings/$', views.UserProfileView.as_view(), name='settings'),
    url(r'^(?P<pk>[0-9]+)/$', views.UserDetailView.as_view(), name='detail'),
    # url(r'^(?P<username>[\w.@+-]+)/posts/$', views.UserPostListView.as_view(), name='posts'),
    # url(r'^(?P<username>[\w.@+-]+)/replies/$', views.UserReplyListView.as_view(), name='replies'),
]
