from django.db import models
from django.conf import settings


class WebOperator(models.Model):
    """
    A web operator has limited access to console commands
    via a web interface.

    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='webop')

    last_x = models.BigIntegerField(default=0)
    last_y = models.IntegerField(default=0)
    last_z = models.BigIntegerField(default=0)

    class Meta:
        verbose_name = 'Web Operator'
        verbose_name_plural = 'Web Operators'
        ordering = ['user']
        permissions = [
            ('gamemode_spectator', "User can change to spectator mode."),
            ('player_kick', "Can kick players."),
            ('player_ban', "Can ban players."),
            ('player_banip', "Can ban players by IP."),
        ]

    def __str__(self):
        return self.user.username
