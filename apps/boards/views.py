from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.utils.functional import cached_property
from vanilla import ListView, DetailView, CreateView, UpdateView, RedirectView
from pure_pagination import Paginator
from utils.views import UserFormKwargsMixin, SuccessMessageMixin
from .forms import ThreadCreateForm, PostCreateForm, PostUpdateForm
from .models import Board, Thread, Post


class BoardListView(ListView):
    model = Board
    lookup_field = 'board'
    context_object_name = 'boards'

    def get_queryset(self):
        return Board.objects.get_visible_for_user(self.request.user)

board_list = BoardListView.as_view()


class ThreadView(object):
    model = Thread

    def get_queryset(self):
        return Thread.objects.filter(board=self.board)

    @cached_property
    def board(self):
        qs = Board.objects.get_visible_for_user(self.request.user)
        return get_object_or_404(qs, slug=self.kwargs['board'])

    def get_context_data(self, **kwargs):
        kwargs.update({
            'board': self.board,
        })
        return super(ThreadView, self).get_context_data(**kwargs)


class PurePaginator(object):
    def get_paginator(self, queryset, page_size):
        return Paginator(queryset, page_size, request=self.request)


class ThreadListView(ThreadView, PurePaginator, ListView):
    context_object_name = 'threads'
    paginate_by = Thread.THREADS_PER_PAGE

    def user_can_create_thread(self):
        return self.board.can_create_thread(self.request.user)

thread_list = ThreadListView.as_view()


class ThreadCreateView(ThreadView, UserFormKwargsMixin, SuccessMessageMixin, CreateView):
    model = Thread
    form_class = ThreadCreateForm

    success_message = "New thread created, you can see it below."

    def dispatch(self, request, *args, **kwargs):
        if not self.board.can_create_thread(request.user):
            messages.add_message(request, messages.ERROR,
                                 "You don't have permission to create threads here.")
            return redirect(self.board.get_absolute_url())
        return super(ThreadCreateView, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        kwargs.update({'board': self.board})
        return super(ThreadCreateView, self).get_form(*args, **kwargs)

thread_create = login_required(ThreadCreateView.as_view())


class PostView(object):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(thread=self.thread).prefetch_related('user')

    @cached_property
    def thread(self):
        boards = Board.objects.get_visible_for_user(self.request.user)
        qs = Thread.objects.filter(board__in=boards)
        return get_object_or_404(qs, slug=self.kwargs['thread'])

    def get_context_data(self, **kwargs):
        kwargs.update({
            'thread': self.thread,
        })
        return super(PostView, self).get_context_data(**kwargs)


class PostListView(PostView, PurePaginator, ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = Post.POSTS_PER_PAGE

    def user_can_post(self):
        return self.thread.can_reply(self.request.user)

post_list = PostListView.as_view()


class LatestPostListView(RedirectView):
    """
    Redirect to the last page of a thread.

    """
    def get_redirect_url(self, thread, post=None):

        url = reverse('boards:post_list', kwargs={'thread': thread})

        thread_obj = get_object_or_404(Thread, slug=thread)
        last_page = thread_obj.get_last_page()

        if post is not None:
            return '{}?page={}#post-{}'.format(url, last_page, post)
        return '{}?page={}'.format(url, last_page)

post_latest = LatestPostListView.as_view()


class PostCreateView(PostView, UserFormKwargsMixin, SuccessMessageMixin, CreateView):
    form_class = PostCreateForm

    success_message = "Post created, you can see it below."

    def dispatch(self, request, *args, **kwargs):
        if not self.thread.can_reply(request.user):
            messages.add_message(request, messages.ERROR,
                                 "You don't have permission to reply to this thread.")
            return redirect(self.thread.get_absolute_url())
        return super(PostCreateView, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        kwargs.update({'thread': self.thread})
        return super(PostCreateView, self).get_form(*args, **kwargs)

post_create = login_required(PostCreateView.as_view())


class PostUpdateView(PostView, UserFormKwargsMixin, SuccessMessageMixin, UpdateView):
    form_class = PostUpdateForm
    object = None

    success_message = "Post updated, you can see it below."

    def get_object(self):
        if not self.object:
            self.object = super(PostUpdateView, self).get_object()
        return self.object

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().can_update(request.user):
            messages.add_message(request, messages.ERROR,
                                 "You don't have permission to update this post.")
            return redirect(self.thread.get_absolute_url())
        return super(PostUpdateView, self).dispatch(request, *args, **kwargs)

post_update = login_required(PostUpdateView.as_view())


class PostHistoryView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name_suffix = '_history'

post_history = permission_required('boards.view_history')(PostHistoryView.as_view())
