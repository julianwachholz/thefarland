from django.db import models
from django.db.models import Q


class BoardManager(models.Manager):
    """
    Manager for discussion boards.

    """
    def get_visible_for_user(self, user):
        if user.is_superuser:
            return self.all()

        return self.filter(
            Q(group_view=None) | Q(group_view__in=user.groups.all())
        )
