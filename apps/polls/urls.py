from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.poll_list, name='list'),
    url(r'^vote/$', views.poll_vote, name='vote'),
    url(r'^view/(?P<slug>[\w-]+)/$', views.poll_detail, name='detail'),
]
