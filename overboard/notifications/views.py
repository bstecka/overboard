from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.http import HttpResponseRedirect
from .models import UserNotification

# Create your views here.


def notification_visited(request, pk):
    notification = get_object_or_404(UserNotification, pk=pk)
    question_id = notification.related_question.pk
    notification.delete()
    return HttpResponseRedirect(reverse('posts:question_page', args=(question_id,)))


def delete(request, pk):
    get_object_or_404(UserNotification, pk=pk).delete()
    return HttpResponseRedirect('')
