from django.apps import AppConfig
from . import signals


class ShopAppConfig(AppConfig):
    name = 'apps.shop'

    def ready(self):
        from paypal.standard.ipn.signals import payment_was_successful
        payment_was_successful.connect(signals.payment_received, dispatch_uid='shop.payment_received')
