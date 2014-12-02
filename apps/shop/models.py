from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from autoslug import AutoSlugField


class Product(models.Model):
    CHF = 'CHF'
    CURRENCIES = [
        (CHF, 'CHF'),
    ]

    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True)
    subtitle = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCIES, default=CHF)

    instant_delivery = models.BooleanField(default=False)
    delivery_command = models.TextField(blank=True)

    redeem_notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['amount']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_order', kwargs={'pk': self.pk})


class Order(models.Model):
    """
    Simple orders, one Product at a time.

    """
    UNPAID = 0
    PAID = 1
    ERROR = 2
    STATUS = [
        (UNPAID, 'Waiting for payment...'),
        (PAID, 'Paid'),
        (ERROR, 'Error'),
    ]
    product = models.ForeignKey(Product, related_name='orders')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders')
    status = models.IntegerField(choices=STATUS, default=UNPAID)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)
    redeemed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return 'Order #{}'.format(self.pk)

    def get_absolute_url(self):
        return reverse('shop:order_detail', kwargs={'pk': self.pk})

    def needs_payment(self):
        return self.status == Order.UNPAID

    def can_redeem(self):
        return not self.redeemed and self.status == Order.PAID and self.product.instant_delivery
