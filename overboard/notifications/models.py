from django.db import models
from django.contrib.auth.models import User
from posts.models import Question


class Notification(models.Model):
    title = models.CharField(max_length=200, default='')


class UsersNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, null=True)
    notif_date = models.DateTimeField('date received')
    related_question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=200, default='')
    title = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.user.__str__() + ' ' + self.notification.__str__()


class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, null=True)
    notif_date = models.DateTimeField('date received')
    related_question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=200, default='')
    title = models.CharField(max_length=200, default='')

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.__str__() + ' ' + self.notification.__str__()


class UserNotificationNewAnswer(UserNotification):
#    answering_user = models.CharField(max_length=200, default='')

    def save(self, *args, **kwargs):
        self.title = 'New answer'
        self.content = ' answered your question ' + self.related_question.__str__()
        super(UserNotificationNewAnswer, self).save(*args, **kwargs)
