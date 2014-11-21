from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from . import commands


class WebOperator(models.Model):
    """
    A web operator has limited access to console commands
    via a web interface.

    """
    SURVIVAL = 0
    CREATIVE = 1
    ADVENTURE = 2
    SPECTATOR = 3

    GAMEMODE_CHOICES = [
        (SURVIVAL, 'Survival'),
        (CREATIVE, 'Creative'),
        (ADVENTURE, 'Adventure'),
        (SPECTATOR, 'Spectator'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='webop')

    last_x = models.BigIntegerField(default=0)
    last_y = models.IntegerField(default=0)
    last_z = models.BigIntegerField(default=0)

    gamemode = models.IntegerField(choices=GAMEMODE_CHOICES, default=SURVIVAL)

    class Meta:
        verbose_name = 'Web Operator'
        verbose_name_plural = 'Web Operators'
        ordering = ['user']
        permissions = [
            ('is_op', "Can access WebOp panel."),
            ('gamemode_spectator', "User can change to spectator mode."),
            ('player_kick', "Can kick players."),
            ('player_ban', "Can ban players."),
            ('player_banip', "Can ban players by IP."),
        ]

    def __str__(self):
        return self.user.username

    @cached_property
    def username(self):
        return self.user.username

    def log_action(self, action, arguments=None):
        if arguments is None:
            arguments = ''
        self.log.create(action=action, arguments=arguments)

    def query_coords(self, save=False):
        """
        Ask Minecraft for player's current coordinates.

        """
        coords = commands.query_player_coords(self.username)
        if save and coords:
            self.set_coords(coords)
        return coords

    def set_coords(self, coords):
        self.last_x = coords['x']
        self.last_y = coords['y']
        self.last_z = coords['z']

    def get_coords(self):
        return {
            'x': self.last_x,
            'y': self.last_y,
            'z': self.last_z,
        }
    get_coords.short_description = 'Last position'

    def tp(self, coords):
        commands.tp_player(self.username, **coords)

    def is_spectator(self):
        return self.gamemode == WebOperator.SPECTATOR

    def go_spectator(self):
        self.gamemode = WebOperator.SPECTATOR
        commands.change_gamemode(self.username, WebOperator.SPECTATOR)

    def go_survival(self):
        self.gamemode = WebOperator.SURVIVAL
        commands.change_gamemode(self.username, WebOperator.SURVIVAL)


class LogAction(models.Model):
    """
    Log WebOperator actions.

    """
    webop = models.ForeignKey(WebOperator, related_name='log')
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=500)
    arguments = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Log Action'
        verbose_name_plural = 'Log Actions'
        ordering = ['-timestamp']
