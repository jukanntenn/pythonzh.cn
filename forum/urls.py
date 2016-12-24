from django.conf.urls import url

from . import views

app_name = 'forum'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^new/(?:(?P<slug>[\w-]+)/)?$', views.PostCreateView.as_view(), name='create'),
    # url(r'^post/(?P<slug>[\w-]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.PostEditView.as_view(), name='edit'),
    url(r'^notifications/$', views.NotificationsListView.as_view(), name='all'),
]
