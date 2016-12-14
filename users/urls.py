from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url(r'^(?P<username>.+)/profile_change/$', views.UserProfileChangeView.as_view(), name='profile_change'),
    url(r'^(?P<username>.+)/mugshot_change/$', views.MugshotChangeView.as_view(), name='mugshot_change'),
    url(r'^(?P<username>.+)/$', views.UserDetailView.as_view(), name='detail'),
]
