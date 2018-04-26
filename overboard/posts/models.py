from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.


class Vote(models.Model):
    vote_date = models.DateTimeField('date voted')
    voter = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    value = models.IntegerField()
    limit = models.Q(app_label='core', model='question') | \
        models.Q(app_label='core', model='answer')
    content_type = models.ForeignKey(
        ContentType,
        limit_choices_to=limit,
        null=True,
        on_delete=models.CASCADE,
        blank=True,
    )
    object_id = models.PositiveIntegerField(
        null=True,
    )
    target = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return 'Vote on ' + self.target.__str__()


class Question(models.Model):
    title = models.CharField(max_length=200, default='')
    content = models.CharField(max_length=600, default='')
    pub_date = models.DateTimeField(default=datetime.now, blank=True)
    asked_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    votes = GenericRelation(Vote)

    @property
    def all_vote_set(self):
        votes_all = Vote.objects.all()
        return votes_all

    def __str__(self):
        return 'Question ' + self.title.__str__()


class Answer(models.Model):
    published_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=600, default='')
    pub_date = models.DateTimeField(default=datetime.now, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    accepted = models.BooleanField()
    votes = GenericRelation(Vote)

    def __str__(self):
        return 'Answer to ' + self.question.__str__()
