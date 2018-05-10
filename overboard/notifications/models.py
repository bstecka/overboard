from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    notification_text = models.CharField(max_length=200)
    notification_type = models.CharField(max_length=200)

    def __str__(self):
        return self.notification_text


class UsersNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    notif_date = models.DateTimeField('date received')

    def __str__(self):
        return self.user.__str__() + ' ' + self.notification.__str__()
