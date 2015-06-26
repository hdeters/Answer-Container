from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Q


class Profile(models.Model):
    user = models.OneToOneField(User, null=True)
    bio = models.TextField()

    @property
    def get_score(self):
        score = 0
        question_count = self.question_set.count()
        score += (5 * question_count)
        # answers = self.answer_set.all().values('vote').annotate(up_votes=Count(upvote=True, distinct=True),
        #                                                         down_votes=Count(upvote=False, distinct=True))
        # score += (10 * answers.up_votes)
        # score -= (5 * answers.down_votes)

        downvoted_answers = self.vote_set.filter(upvote=False).count()
        score -= downvoted_answers

        return score

    def __str__(self):
        return str(self.user)
