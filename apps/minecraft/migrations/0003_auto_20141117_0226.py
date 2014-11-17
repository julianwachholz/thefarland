# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('minecraft', '0002_auto_20141117_0121'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weboperator',
            options={'ordering': ['user'], 'permissions': [('is_op', 'Can access WebOp panel.'), ('gamemode_spectator', 'User can change to spectator mode.'), ('player_kick', 'Can kick players.'), ('player_ban', 'Can ban players.'), ('player_banip', 'Can ban players by IP.')], 'verbose_name_plural': 'Web Operators', 'verbose_name': 'Web Operator'},
        ),
    ]
