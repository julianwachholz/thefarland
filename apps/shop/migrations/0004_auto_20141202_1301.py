# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20141201_1921'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': 'Products', 'verbose_name': 'Product', 'ordering': ['amount']},
        ),
        migrations.AddField(
            model_name='product',
            name='redeem_notes',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(0, 'Waiting for payment...'), (1, 'Paid'), (2, 'Error')], default=0),
            preserve_default=True,
        ),
    ]
