from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Q


class Profile(models.Model):
    user = models.OneToOneField(User, null=True)
    bio = models.TextField()

    @property
    def get_score(self):
        from QandA.models import Vote
        from QandA.models import Question

        score = 0
        qs_with_as = Question.objects.filter(~Q(accepted_answer=None))
        accepted_answer_pks = [q.accepted_answer for q in qs_with_as]
        accepted_list = self.answer_set.filter(id__in=accepted_answer_pks)
        if accepted_list:
            score += 100

        question_count = self.question_set.count()
        score += (5 * question_count)

        good = Vote.objects.filter(answer__profile=self, upvote=True).count()
        bad = Vote.objects.filter(answer__profile=self, upvote=False).count()

        score += (10 * good)
        score -= (5 * bad)

        downvoted_answers = self.vote_set.filter(upvote=False).count()
        score -= downvoted_answers

        return score

    def __str__(self):
        return str(self.user)
