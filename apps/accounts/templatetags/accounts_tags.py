import re

from django import template

from social.backends.oauth import OAuthAuth


register = template.Library()


@register.filter
def social_account(social_auth):
    """
    Returns the username for a given social auth object.

    """
    return {
        'mineid': lambda s: s.name,
        'facebook': lambda s: s.extra_data['name'],
        'twitter': lambda s: '@{0}'.format(s.extra_data['access_token']['screen_name']),
        'google-plus': lambda s: s.uid,
    }.get(social_auth.provider)(social_auth)


@register.filter
def backend_name(name):
    """
    Get a nice human-readable string back for this backend identifier.

    """
    return {
        'mineid': 'MineID.org',
        'facebook': 'Facebook',
        'twitter': 'Twitter',
        'google-plus': 'Google+',
    }.get(name, name)


@register.filter
def icon_name(name):
    return {
        'mineid': 'minecraft',
        'google-plus': 'google',
        'facebook': 'facebook',
        'twitter': 'twitter',
    }.get(name, name)
