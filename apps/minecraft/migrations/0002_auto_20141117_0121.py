# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('minecraft', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='weboperator',
            name='last_x',
            field=models.BigIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='weboperator',
            name='last_y',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='weboperator',
            name='last_z',
            field=models.BigIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='weboperator',
            name='user',
            field=models.OneToOneField(related_name='webop', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
