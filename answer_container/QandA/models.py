from django.db import models

from users.models import Profile


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    profile = models.ForeignKey(Profile)
    timestamp = models.DateTimeField(null=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    text = models.TextField()
    questions = models.ManyToManyField('Question')


class AnswerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('vote_set')


class Answer(models.Model):
    text = models.TextField()
    profile = models.ForeignKey(Profile)
    question = models.ForeignKey('Question')
    score = models.IntegerField(default=0)

    objects = AnswerManager()

    def set_score(self):
        if self.vote_set.exists():
            self.score = self.vote_set.filter(upvote=True).count() - \
                   self.vote_set.filter(upvote=False).count()
        else:
            self.score = 0


class Vote(models.Model):
    profile = models.ForeignKey(Profile)
    answer = models.ForeignKey('Answer')
    upvote = models.BooleanField(default=True)

    class Meta:
        unique_together = ('profile', 'answer',)
