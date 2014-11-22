from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from vanilla import ListView, DetailView, CreateView
from utils.views import UserFormKwargsMixin, SuccessMessageMixin
from .forms import ThreadCreateForm
from .models import Board, Thread, Post


class BoardView(object):
    model = Board
    lookup_field = 'slug'

    def get_queryset(self):
        return Board.objects.get_visible_for_user(self.request.user)


class BoardListView(BoardView, ListView):
    context_object_name = 'boards'

board_list = BoardListView.as_view()


class BoardDetailView(BoardView, DetailView):
    context_object_name = 'board'

    def user_can_create_thread(self):
        return self.object.can_create_thread(self.request.user)

board_detail = BoardDetailView.as_view()


class ThreadDetailView(DetailView):
    model = Thread
    lookup_field = 'slug'
    context_object_name = 'thread'

    def user_can_post(self):
        return self.object.can_reply(self.request.user)

thread_detail = ThreadDetailView.as_view()


class ThreadCreateView(UserFormKwargsMixin, SuccessMessageMixin, CreateView):
    model = Thread
    form_class = ThreadCreateForm

    success_message = "New thread created, you can see it below."

    @cached_property
    def board(self):
        return get_object_or_404(Board, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        kwargs.update({
            'board': self.board,
        })
        return super(ThreadCreateView, self).get_context_data(**kwargs)

    def get_form(self, *args, **kwargs):
        kwargs.update({'board': self.board})
        return super(ThreadCreateView, self).get_form(*args, **kwargs)

thread_create = ThreadCreateView.as_view()
