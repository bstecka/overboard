from django.db import models
from django.contrib.auth.models import User
from posts.models import Question, Answer
from datetime import datetime


class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notif_date = models.DateTimeField('date received', default=datetime.now)
    content = models.CharField(max_length=200, default='')
    title = models.CharField(max_length=200, default='')

    class Meta:
        abstract = True


class NotificationManager(models.Manager):
    def create_notification(self, answer):
        return UserNotificationNewAnswer.create(answer=answer)


class UserNotificationNewAnswer(UserNotification):
    related_question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    objects = NotificationManager()

    @classmethod
    def create(cls, answer):
        notification = cls(
            user=answer.question.asked_by,
            related_question=answer.question,
            title='New answer',
            content=answer.published_by.__str__() + ' answered your question ' + answer.question.__str__()
        )
        return notification
