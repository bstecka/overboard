from django.db import models
from django.contrib.auth.models import User
from posts.models import Question, Answer
from datetime import datetime


class NotificationManager(models.Manager):
    def create_notification_for_new_answer(self, answer):
        return UserNotification.create_for_new_answer(answer=answer)

    def create_notification_for_popular_question(self, question):
        return UserNotification.create_for_popular_question(question=question)

    def create_notification_for_popular_answer(self, answer):
        return UserNotification.create_for_popular_answer(answer=answer)


class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notif_date = models.DateTimeField('date received', default=datetime.now)
    content = models.CharField(max_length=200, default='')
    title = models.CharField(max_length=200, default='')
    related_question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    related_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    objects = NotificationManager()

    @classmethod
    def create_for_new_answer(cls, answer):
        notification = cls(
            user=answer.question.asked_by,
            related_question=answer.question,
            title='New answer',
            content=answer.published_by.__str__() + ' answered your question ' + answer.question.__str__()
        )
        return notification

    @classmethod
    def create_for_popular_question(cls, question):
        notification = cls(
            user=question.asked_by,
            related_question=question,
            title='Popular question',
            content='Your question is popular! '
        )
        return notification

    @classmethod
    def create_for_popular_answer(cls, answer):
        notification = cls(
            user=answer.question.asked_by,
            related_question=answer.question,
            title='Popular answer',
            content='Your answer is popular!'
        )
        return notification

    def save(self, *args, **kwargs):
        super(UserNotification, self).save(*args, **kwargs)
        notifications = self.related_question.usernotification_set.order_by('notif_date')
        if notifications.count() > 2:
            notifications[0].delete()




