 # core/views.py
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.db.models import Count, Sum, Q
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.views import View
from .models import Question, Tag, Vote, Answer
from .forms import AnswerForm, VoteForm, AnswerVoteForm, NewQuestionForm
import datetime


def latest_question_list(request):
    latest_questions = Question.objects.all().order_by('-pub_date')
    return render(request, 'index_content.html', {'questions': latest_questions, 'selected_tab': 'last'})


def top_questions(delta_time):
    from_date = datetime.datetime.now() - datetime.timedelta(days=delta_time)
    questions = Question.objects.filter(pub_date__range=[from_date, datetime.datetime.now()]).annotate(number_of_votes=Count('votes'))
    return questions.order_by('-number_of_votes')


def top_week_questions(request):
    return render(request, 'index_content.html', {'questions': top_questions(7), 'selected_tab': 'week'})


def top_month_questions(request):
    return render(request, 'index_content.html', {'questions': top_questions(30), 'selected_tab': 'month'})


def search(request):
    if request.GET:
        phrase = request.GET.get("input_search_phrase")
        questions = Question.objects.filter(Q(title__contains=phrase) | Q(content__contains=phrase))
        return render(request, 'search_question.html', {'questions': questions, 'phrase': phrase})
    return render(request, 'index')

