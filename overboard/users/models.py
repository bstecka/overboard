from django.db import models
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


class Badge(models.Model):
    badge_name = models.CharField(max_length=200)

    def __str__(self):
        return self.badge_name


class UsersBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__() + ' ' + self.badge.__str__()
