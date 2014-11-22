from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.board_list, name='list'),
    url(r'^(?P<board>[\w-]+)/$', views.thread_list, name='thread_list'),
    url(r'^(?P<board>[\w-]+)/new/$', views.thread_create, name='thread_create'),
    url(r'^(?P<thread>[\w-]+/[\w-]+)/$', views.post_list, name='post_list'),
    url(r'^(?P<thread>[\w-]+/[\w-]+)/reply/$', views.post_create, name='post_create'),
    url(r'^(?P<thread>[\w-]+/[\w-]+)/latest/$', views.post_latest, name='post_latest'),
    url(r'^(?P<thread>[\w-]+/[\w-]+)/latest/(?P<post>\d+)/$', views.post_latest, name='post_latest'),
]
