# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0009_post_is_modified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='is_modified',
            field=models.BooleanField(editable=False, default=False),
            preserve_default=True,
        ),
    ]
