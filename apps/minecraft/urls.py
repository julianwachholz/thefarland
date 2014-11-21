from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^webop/$', views.webop, name='webop'),
    url(r'^webop/spectator/$', views.spectator, name='spectator'),
    url(r'^webop/spectator/go/$', views.gamemode_spectator, name='gamemode_spectator'),
]
