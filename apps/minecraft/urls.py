from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^webop/$', views.webop, name='webop'),
    url(r'^webop/spectator/$', views.spectator, name='spectator'),
    url(r'^webop/spectator/coords/$', views.get_coords, name='get_coords'),
]
