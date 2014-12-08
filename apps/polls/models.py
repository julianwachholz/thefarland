from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.timezone import now
from autoslug import AutoSlugField


class PollManager(models.Manager):

    def get_queryset(self):
        qs = super(PollManager, self).get_queryset()
        return qs.filter(
            start__lte=now(),
            end__gt=now()
        )


class Poll(models.Model):
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name', unique=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    start = models.DateTimeField()
    end = models.DateTimeField()

    objects = models.Manager()
    active = PollManager()

    class Meta:
        verbose_name = 'Poll'
        verbose_name_plural = 'Polls'
        ordering = ['-created']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('polls:detail', kwargs={'slug': self.slug})

    def did_user_vote(self, user):
        return self.votes.filter(user=user).exists()

    def get_vote_bars(self):
        return self.choices.annotate(count=models.Count('votes'))


class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name='choices')
    name = models.CharField(max_length=200)
    ordering = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'
        ordering = ['ordering', 'name']

    def __str__(self):
        return self.name


class Vote(models.Model):
    poll = models.ForeignKey(Poll, related_name='votes')
    choice = models.ForeignKey(Choice, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='poll_votes+')

    class Meta:
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'
        unique_together = ['poll', 'user']

    def __str__(self):
        return 'Vote #{}'.format(self.pk)

    def get_absolute_url(self):
        return self.poll.get_absolute_url()
