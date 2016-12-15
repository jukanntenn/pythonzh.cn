from django.conf.urls import url

from . import views

app_name = 'forum'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^new/$', views.PostCreateView.as_view(), name='create'),
    url(r'^post/(?P<slug>[\w-]+)/$', views.PostDetailView.as_view(), name='detail'),
]
