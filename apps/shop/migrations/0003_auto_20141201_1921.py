# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Product', 'verbose_name_plural': 'Products', 'ordering': ['-amount']},
        ),
        migrations.AddField(
            model_name='order',
            name='notes',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
    ]
