from django import forms
from utils.forms import SaveKwargsPopMixin, KwargsPopMixin
from markdown_deux.templatetags.markdown_deux_tags import markdown_allowed
from .models import Thread, Post


class ThreadCreateForm(SaveKwargsPopMixin, KwargsPopMixin, forms.ModelForm):
    """
    Create a new thread in a board.

    """
    contents = forms.CharField(label='Content', widget=forms.Textarea,
                               help_text=markdown_allowed(), required=True)

    pop_kwargs = ['user', 'board']

    class Meta:
        model = Thread
        fields = ['name']

    def save(self, commit=True):
        thread = super(ThreadCreateForm, self).save(commit)
        thread.posts.create(
            user=thread.user,
            content=self.cleaned_data['contents'],
        )
        return thread
