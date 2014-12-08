# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.shop.validators
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20141202_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='can_deliver',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_command',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='fields',
            field=jsonfield.fields.JSONField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='fields',
            field=jsonfield.fields.JSONField(blank=True, null=True, validators=[apps.shop.validators.product_fields_validator]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(0, 'Waiting for payment...'), (1, 'Paid'), (2, 'Error'), (3, 'Canceled'), (4, 'Delivered')], default=0),
            preserve_default=True,
        ),
    ]
