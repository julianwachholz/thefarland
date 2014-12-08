import logging
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.urlresolvers import reverse
from django.db import models
from django import forms
from autoslug import AutoSlugField
from jsonfield import JSONField
from .validators import ALPHANUMERIC, product_fields_validator


logger = logging.getLogger(__name__)


class ActiceProductManager(models.Manager):

    def get_queryset(self):
        qs = super(ActiceProductManager, self).get_queryset()
        return qs.filter(is_active=True)


class Product(models.Model):
    CHF = 'CHF'
    CURRENCIES = [
        (CHF, 'CHF'),
    ]

    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True)
    subtitle = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCIES, default=CHF)
    monthly = models.BooleanField(default=False)

    instant_delivery = models.BooleanField(default=False)
    delivery_command = models.TextField(blank=True)
    fields = JSONField(blank=True, null=True, validators=[product_fields_validator])
    redeem_notes = models.TextField(blank=True)

    objects = models.Manager()
    active = ActiceProductManager()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['amount']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_order', kwargs={'pk': self.pk})

    def get_form_fields(self):
        for field in self.fields:
            help_text = field.get('help_text', '')
            if field['field_type'] in ('alpha', 'email'):
                alpha = field['field_type'] == 'alpha'
                field_class = forms.CharField if alpha else forms.EmailField
                form_field = field_class(
                    label=field['display'],
                    help_text=help_text,
                    max_length=getattr(field, 'max', 255),
                    validators=[ALPHANUMERIC] if alpha else []
                )
            elif field['field_type'] == 'number':
                form_field = forms.IntegerField(label=field['display'], help_text=help_text, validators=[
                    MinValueValidator(getattr(field, 'min', 0)),
                    MaxValueValidator(getattr(field, 'max', 100)),
                ])
            yield field['name'], form_field


class Order(models.Model):
    """
    Simple orders, one Product at a time.

    """
    UNPAID = 0
    PAID = 1
    ERROR = 2
    CANCELED = 3
    DELIVERED = 4
    STATUS = [
        (UNPAID, 'Waiting for payment...'),
        (PAID, 'Paid'),
        (ERROR, 'Error'),
        (CANCELED, 'Canceled'),
        (DELIVERED, 'Delivered'),
    ]
    product = models.ForeignKey(Product, related_name='orders')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders')
    status = models.IntegerField(choices=STATUS, default=UNPAID)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)
    fields = JSONField(blank=True, null=True)
    can_deliver = models.BooleanField(default=False)
    delivery_command = models.TextField(blank=True)
    redeemed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created']

    def __str__(self):
        return 'Order #{}'.format(self.pk)

    def save(self, **kwargs):
        if self.product.instant_delivery:
            self.can_deliver = True
        if not self.delivery_command:
            self.delivery_command = self.product.delivery_command
        return super(Order, self).save(**kwargs)

    def get_absolute_url(self):
        return reverse('shop:order_detail', kwargs={'pk': self.pk})

    def needs_payment(self):
        return self.status == Order.UNPAID

    def can_redeem(self):
        return self.can_deliver and self.status == Order.PAID

    def deliver(self):
        """
        Parse the delivery_command with all variables.

        """
        from apps.minecraft.tasks import minecraft_cmd

        template = self.delivery_command
        tpl_args = self.fields
        tpl_args.update({
            'user': self.user.username,
        })

        command = template % tpl_args
        logger.info("Executed delivery command: '%s'" % command)
        minecraft_cmd.delay(command)

        self.status = Order.DELIVERED
        self.redeemed = True
