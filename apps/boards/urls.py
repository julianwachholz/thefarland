from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.board_list, name='list'),
    url(r'^(?P<slug>[\w-]+)/$', views.board_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/new/$', views.thread_create, name='thread_create'),
    url(r'^(?P<slug>[\w-]+/[\w-]+)/$', views.thread_detail, name='thread'),
]
