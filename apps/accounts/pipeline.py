from django.shortcuts import redirect
from social.pipeline.partial import partial


@partial
def minecraft_name(strategy, details, user=None, is_new=False, *args, **kwargs):
    """
    Users should enter their Minecraft username.

    """
    if user and user.username:
        return
    elif is_new and not details.get('username'):
        username = strategy.request_data().get('username')
        if email:
            details['username'] = username
        else:
            return redirect('accounts:minecraft_name')
