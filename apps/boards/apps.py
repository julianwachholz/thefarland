from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete
from . import signals


class BoardsAppConfig(AppConfig):
    name = 'apps.boards'

    def ready(self):
        Board = self.get_model('Board')
        Thread = self.get_model('Thread')
        Post = self.get_model('Post')

        post_save.connect(signals.thread_post_save, sender=Thread)
        post_save.connect(signals.post_post_save, sender=Post)
        post_delete.connect(signals.thread_post_delete, sender=Thread)
