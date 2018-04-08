from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class UserExtended(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reputation = models.IntegerField(default=0)

    def __str__(self):
        return self.user.__str__()

    @receiver(post_save, sender=User)
    def create_user_extended(sender, instance, created, **kwargs):
        if created:
            UserExtended.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_extended(sender, instance, **kwargs):
        instance.userextended.save()


class Vote(models.Model):
    vote_date = models.DateTimeField('date voted')
    voter = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    value = models.IntegerField()
    limit = models.Q(app_label='overboardapp', model='question') | \
        models.Q(app_label='overboardapp', model='answer')
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

    @property #EXAMPLE OF PROPERTY REACHABLE IN TEMPLATE
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


class Tag(models.Model):
    tag_name = models.CharField(max_length=200)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.tag_name


class Badge(models.Model):
    badge_name = models.CharField(max_length=200)

    def __str__(self):
        return self.badge_name


class UsersBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__() + ' ' + self.badge.__str__()

#modele notyfikacji do osobnej aplikacji

class Notification(models.Model):
    notification_text = models.CharField(max_length=200)

    def __str__(self):
        return self.notification_text


class UsersNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    notif_date = models.DateTimeField('date received')

    def __str__(self):
        return self.user.__str__() + ' ' + self.notification.__str__()

