from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    score = models.IntegerField(default=0)
    user = models.OneToOneField(User, null=True)

    def __str__(self):
        return str(self.user)
