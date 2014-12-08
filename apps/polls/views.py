from vanilla import ListView, CreateView, DetailView
from django.contrib.auth.decorators import user_passes_test
from utils.views import UserFormKwargsMixin
from apps.accounts.models import user_is_verified
from .models import Poll, Vote
from .forms import VoteForm


class PollView(object):
    model = Poll
    lookup_field = 'slug'

    def get_queryset(self):
        return Poll.active.all()


class PollListView(PollView, ListView):
    context_object_name = 'polls'

poll_list = PollListView.as_view()


class PollDetailView(PollView, DetailView):
    pass

poll_detail = PollDetailView.as_view()


class VoteCreateView(UserFormKwargsMixin, CreateView):
    model = Vote
    form_class = VoteForm

poll_vote = user_passes_test(user_is_verified)(VoteCreateView.as_view())
