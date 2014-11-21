from vanilla import ListView, DetailView
from .models import Board, Thread, Post


class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'

board_list = BoardListView.as_view()


class BoardDetailView(DetailView):
    model = Board
    lookup_field = 'slug'
    context_object_name = 'board'

board_detail = BoardDetailView.as_view()


class ThreadDetailView(DetailView):
    model = Thread
    lookup_field = 'slug'
    context_object_name = 'thread'

thread_detail = ThreadDetailView.as_view()
