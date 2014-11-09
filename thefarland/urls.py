from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from .views import IndexView


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^accounts/', include('apps.accounts.urls', namespace='accounts')),

    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
