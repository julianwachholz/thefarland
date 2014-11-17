from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """
    User manager.

    """
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, **kwargs):
        return self.create_user(is_staff=True, is_superuser=True, **kwargs)


class User(PermissionsMixin, AbstractBaseUser):
    """
    Simple user with username (should be Minecraft username).

    """
    username = models.CharField('Minecraft username', max_length=200, unique=True)
    is_staff = models.BooleanField(default=False)

    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=10, blank=True)

    is_trusted = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    AVATAR_URL = 'https://minotar.net/avatar/{user}/{size}.png'

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def save(self, **kwargs):
        if not self.is_verified and not self.verification_code:
            from random import randint
            self.verification_code = randint(100000, 999999)  # random 6-digit code
        return super(User, self).save(**kwargs)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_avatar_url(self, size=64):
        return self.AVATAR_URL.format(user=self.username, size=size)
