from django.conf.urls import patterns, url
from django.contrib.auth.urls import urlpatterns as auth_patterns
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = patterns(
    '',
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.user_create, name='user_create'),
    url(r'^verify/$', views.verify, name='verify'),
    url(r'^verify/token/$', views.get_verify_token, name='get_verify_token'),
    url(r'^account/$', views.user_update, name='user_update'),
    url(r'^account/password/$', views.password_change, name='password_change'),
)
