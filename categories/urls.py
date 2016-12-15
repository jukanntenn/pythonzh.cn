from django.conf.urls import url

from . import views

app_name = 'categories'
urlpatterns = [
    url(r'^(?P<slug>.+)/$', views.CategoryPostView.as_view(), name='posts'),
]
