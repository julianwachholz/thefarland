# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boards', '0004_auto_20141121_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='user',
            field=models.ForeignKey(related_name='threads', to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=False,
        ),
    ]
