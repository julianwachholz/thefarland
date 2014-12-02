from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^accounts/', include('apps.accounts.urls', namespace='accounts')),
    url(r'^board/', include('apps.boards.urls', namespace='boards')),
    url(r'^shop/', include('apps.shop.urls', namespace='shop')),
    url(r'^mc/', include('apps.minecraft.urls', namespace='minecraft')),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
