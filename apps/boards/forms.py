from django import forms
from django.core.validators import MinLengthValidator
from utils.forms import SaveKwargsPopMixin, KwargsPopMixin
from .models import Thread, Post


HELP_TEXT = """
<a href="http://daringfireball.net/projects/markdown/syntax" tabindex="-1" target="_blank">Markdown syntax</a> allowed,
but no raw HTML. Examples: **bold**, *italic*, [Link](http://thefar.land/).
"""

CONTENT_FIELD = forms.CharField(label='Content', widget=forms.Textarea,
                                validators=[MinLengthValidator(17)],
                                help_text=HELP_TEXT, required=True)


class ThreadCreateForm(SaveKwargsPopMixin, KwargsPopMixin, forms.ModelForm):
    """
    Create a new thread in a board.

    """
    contents = CONTENT_FIELD

    pop_kwargs = ['user', 'board']

    class Meta:
        model = Thread
        fields = ['name']

    def save(self, commit=True):
        thread = super(ThreadCreateForm, self).save(commit)
        thread.posts.create(
            user=thread.user,
            contents=self.cleaned_data['contents'],
        )
        return thread


class PostCreateForm(SaveKwargsPopMixin, KwargsPopMixin, forms.ModelForm):
    """
    Submit a new reply to a thread.

    """
    contents = CONTENT_FIELD

    pop_kwargs = ['user', 'thread']

    class Meta:
        model = Post
        fields = ['contents']


class PostUpdateForm(KwargsPopMixin, forms.ModelForm):
    """
    Modify an existing post.

    """
    contents = CONTENT_FIELD
    reason = forms.CharField(label="Reason for edit", required=False)

    class Meta:
        model = Post
        fields = ['contents']

    def save(self, commit=True):
        post = super(PostUpdateForm, self).save(commit=False)
        post.is_modified = True
        post.history.create(
            user=self.user,
            reason=self.cleaned_data['reason'],
            created=self.instance.updated,
            contents=self.instance.contents,
        )
        post.save()
        return post
