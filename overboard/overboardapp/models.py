from django.db import models
from django.utils.timezone import utc
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.


class Post(models.Model):
    content = models.CharField(max_length=600, default='')
    pub_date = models.DateTimeField('date published')
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.content

    def get_time_diff(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        timediff = now - self.pub_date
        return timediff.total_seconds()

    def get_votes(self):
        Vote.objects.filter(post=self)


class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reputation = models.IntegerField()

    def __str__(self):
        return self.user.__str__();


class Question(models.Model):
    title = models.CharField(max_length=200, default='')
    content = models.CharField(max_length=600, default='')
    pub_date = models.DateTimeField(default=datetime.now, blank=True)
    asked_by = models.ForeignKey(ExtendedUser, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Answer(models.Model):
    published_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=600, default='')
    pub_date = models.DateTimeField(default=datetime.now, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    accepted = models.BooleanField()

    def __str__(self):
        return 'answer by ' + self.published_by.__str__() + ' to ' + self.question.__str__()


class Tag(models.Model):
    tag_name = models.CharField(max_length=200)

    def __str__(self):
        return self.tag_name


class QuestionsTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.tag.__str__() + ' ' + self.question.__str__()


class Vote(models.Model):
    vote_date = models.DateTimeField('date voted')
    voter = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    value = models.IntegerField()

    def __str__(self):
        return 'vote'


class Badge(models.Model):
    badge_name = models.CharField(max_length=200)

    def __str__(self):
        return self.badge_name


class UsersBadge(models.Model):
    user = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__() + ' ' + self.badge.__str__()


class Notification(models.Model):
    notification_text = models.CharField(max_length=200)

    def __str__(self):
        return self.notification_text


class UsersNotification(models.Model):
    user = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    notif_date = models.DateTimeField('date received')

    def __str__(self):
        return self.user.__str__() + ' ' + self.notification.__str__()

