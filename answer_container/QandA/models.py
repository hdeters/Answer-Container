from django.db import models

from users.models import Profile


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    profile = models.ForeignKey(Profile)
    timestamp = models.DateTimeField()


class Tag(models.Model):
    text = models.TextField()
    questions = models.ManyToManyField('Question')


class AnswerManager(models.Manager):
    def get_queryset(self):
        return Answer.objects.all().prefetch_related('vote_set')


class Answer(models.Model):
    text = models.TextField()
    profile = models.ForeignKey(Profile)
    question = models.ForeignKey('Question')

    object = AnswerManager()

    @property
    def score(self):
        return self.vote_set.filter(upvote=True).count() - \
               self.vote_set.filter(upvote=False).count()


class Vote(models.Model):
    profile = models.ForeignKey(Profile)
    answer = models.ForeignKey('Answer')
    upvote = models.BooleanField(default=True)
