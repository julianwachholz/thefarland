from vanilla import ListView, CreateView, DetailView
from django.contrib.auth.decorators import login_required
from utils.views import UserFormKwargsMixin
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

poll_vote = login_required(VoteCreateView.as_view())
