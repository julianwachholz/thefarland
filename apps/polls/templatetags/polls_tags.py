import re
from django import template


register = template.Library()


@register.filter
def did_user_vote(poll, user):
    """
    Check if a user voted in a poll.

    """
    return poll.did_user_vote(user)


@register.filter
def vote_percentage(poll, choice):
    if choice.count == 0:
        return 0
    return 100 * poll.votes.count() / choice.count
