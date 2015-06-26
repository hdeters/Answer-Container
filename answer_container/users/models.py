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
        # bad_answers = self.answer_set.annotate(up_votes=Count(vote_set__upvote=True))
        #answers = self.answer_set.annotate(upvotes=Count(upvote=True, distinct=True), downvotes=Count(upvote=False, distinct=True))
        answers = self.answer_set.prefetch_related('vote_set').annotate(upvote=Count(upvote=True))

        # answers = self.answer_set.annotate(up_votes=Count(vote_set__upvote=True, distinct=True),
        #                                    down_votes=Count(vote_set__upvote=False, distinct=True))
        score += (10 * upanswers)
        score -= (5 * downanswers)

        downvoted_answers = self.vote_set.filter(upvote=False).count()
        score -= downvoted_answers

        return score

    def __str__(self):
        return str(self.user)
