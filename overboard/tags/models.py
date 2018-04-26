from django.db import models
from users.models import UserExtended
from posts.models import Question, Vote, Answer


class Tag(models.Model):
    tag_name = models.CharField(max_length=200)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.tag_name
