import re
from django import template


register = template.Library()


@register.filter
def can_update(user, post):
    """
    Check if a user may update a given post.

    """
    return post.can_update(user)
