from faker import Faker
from django.contrib.auth.models import User
import random
import datetime

from users.models import Profile
from QandA.models import Question, Answer, Vote, Tag


def fake():
    faker = Faker()
    for _ in range(5):
        user = User.objects.create(username=faker.first_name(), \
                                   password=faker.last_name())
        profile = Profile.objects.create(user=user)

        for _ in range(5):
            question = Question.objects.create(title=faker.word(), \
                                    text=faker.sentence(), profile=profile, \
                                    timestamp=faker.date_time().replace(\
                                    tzinfo=datetime.timezone(\
                                    offset=datetime.timedelta())))


    for profile in Profile.objects.all():
        for question in profile.question_set.all():
            other = random.choice(Profile.objects.exclude(id=profile.id))
            question.answer_set.create(profile=other, text=faker.sentence())
