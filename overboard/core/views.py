 # core/views.py
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.db.models import Count, Sum, Q
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector
from django.views import View
from django.views.generic import ListView, DetailView
from posts.models import Question, Answer, Vote
from users.models import UserExtended
from tags.models import Tag
from .forms import AnswerForm, VoteForm, AnswerVoteForm, NewQuestionForm
import datetime


class QuestionList(ListView):
    model = Question
    context_object_name = 'questions'
    selected_tab = ''
    template_name = 'index_content.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionList, self).get_context_data(**kwargs)
        context['selected_tab'] = self.selected_tab
        return context

    def get_queryset(self):
        return Question.objects.all().order_by('-pub_date')


class TopQuestionList(QuestionList):
    delta_time = 7

    def get_queryset(self):
        from_date = datetime.datetime.now() - datetime.timedelta(days=self.delta_time)
        questions = Question.objects.filter(pub_date__range=[from_date, datetime.datetime.now()]).annotate(
            number_of_votes=Count('votes'))
        return questions.order_by('-number_of_votes')


''' old views, replaced by TopQuestionList(QUestionList) '''
'''def latest_question_list(request):
    latest_questions = Question.objects.all().order_by('-pub_date')
    return render(request, 'index_content.html', {'questions': latest_questions, 'selected_tab': 'last'})


def top_questions(delta_time):
    from_date = datetime.datetime.now() - datetime.timedelta(days=delta_time)
    questions = Question.objects.filter(pub_date__range=[from_date, datetime.datetime.now()]).annotate(number_of_votes=Count('votes'))
    return questions.order_by('-number_of_votes')


def top_week_questions(request):
    return render(request, 'index_content.html', {'questions': TopQuestionList().get_queryset(), 'selected_tab': 'week'})


def top_month_questions(request):
    return render(request, 'index_content.html', {'questions': TopQuestionList().get_queryset(), 'selected_tab': 'month'})'''



def search(request):
    if request.GET:
        phrase = request.GET.get("input_search_phrase")
        questions = Question.objects.annotate(search=SearchVector('title', 'content')).filter(search=phrase)
        return render(request, 'search_question.html', {'questions': questions, 'phrase': phrase})
    return render(request, 'index')

