from django import forms
from utils.forms import KwargsPopMixin, ManagerKwargsMixin
from .models import Vote


class VoteForm(KwargsPopMixin, ManagerKwargsMixin, forms.ModelForm):

    class Meta:
        model = Vote
        fields = ['poll', 'choice']
