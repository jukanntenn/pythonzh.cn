from django.conf.urls import url

from . import views

app_name = 'replies'
urlpatterns = [
    url(r'^success/$', views.ReplySuccess.as_view(), name='success'),
]
