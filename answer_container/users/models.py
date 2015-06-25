from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, null=True)
    bio = models.TextField()

    @property
    def get_score(self):
        pass

    def __str__(self):
        return str(self.user)
