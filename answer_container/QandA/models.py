from django.db import models

from users.models import Profile


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    profile = models.ForeignKey(Profile)


class Tag(models.Model):
    text = models.TextField()
    questions = models.ManyToManyField('Question')


class Answer(models.Model):
    text = models.TextField()
    profile = models.ForeignKey(Profile)
    question = models.ForeignKey('Question')
    score = models.IntegerField(default=0)


class Vote(models.Model):
    profile = models.ForeignKey(Profile)
    answer = models.ForeignKey('Answer')
    upvote = models.BooleanField(null=True)
