from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.product_list, name='list'),
    url(r'^product/(?P<pk>\d+)/$', views.product_order, name='product_order'),
    url(r'^myorders/$', views.order_list, name='order_list'),
    url(r'^order/(?P<pk>\d+)/$', views.order_detail, name='order_detail'),
    url(r'^order/(?P<pk>\d+)/redeem/$', views.order_redeem, name='order_redeem'),
]
