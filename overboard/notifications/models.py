from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    content = models.CharField(max_length=200, default='')
    title = models.CharField(max_length=200, default='')
    type = models.CharField(max_length=200, default='')
    question_id = models.IntegerField(null=True)

    def __str__(self):
        return self.notification_text


class UsersNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    notif_date = models.DateTimeField('date received')

    def __str__(self):
        return self.user.__str__() + ' ' + self.notification.__str__()
