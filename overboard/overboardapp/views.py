 # overboardapp/views.py
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from .models import Notification, Question, Tag, Vote, UserExtended, Answer
from .forms import AnswerForm, VoteForm, RegistrationForm, NewQuestionForm
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from . import helper_functions as helper
from django.db.models import Q
import datetime


# Create your views here.
class HomePageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(HomePageView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['notification_list'] = Notification.objects.all()
        return context


class PageView(TemplateView):
    template_name = "page.html"

def tag_list(request):
    tags = Tag.objects.all().annotate(num_questions=Count('questions')).order_by('-num_questions')
    return render(request, 'tags.html', {'tags': tags})


def latest_question_list(request):
    latest_questions = Question.objects.all().order_by('-pub_date')[:10]
    return render(request, 'index_content.html', {'questions': helper.default_questions_paginator(request, latest_questions), 'selected_tab': 'last'})


def topweek_question_list(request):
    from_date = datetime.datetime.now() - datetime.timedelta(days=7)
    latest_questions = Question.objects.filter(pub_date__range=[from_date, datetime.datetime.now()]).order_by('-pub_date')[:10]
    return render(request, 'index_content.html', {'questions': latest_questions, 'selected_tab': 'week'})


def question_detail(request, question_id):   # Page with details of question
    question = get_object_or_404(Question, pk=question_id)
    vote_sum = question.votes.all().aggregate(Sum('value'))
    previous_vote = 0
    user_f = User.objects.filter(username=request.user.get_username()).first()
    user_extended_f = UserExtended.objects.filter(user=user_f).first()
    for v in question.votes.all():
        if v.voter == user_extended_f:
            previous_vote = v.value
    if request.POST:
        form = VoteForm(request.POST)
        answer_form = AnswerForm(request.POST)
        if form.is_valid():
            value = form.cleaned_data['vote']
            found_duplicate_vote = False
            found_opposite_vote = False
            found_vote = Vote.objects.first()
            for v in question.votes.all():
                if v.voter == user_extended_f and v.value == value:
                    found_duplicate_vote = True
                    found_vote = v
                elif v.voter == user_extended_f:
                    found_opposite_vote = True
                    found_vote = v
            if found_duplicate_vote or found_opposite_vote:
                found_vote.delete()
            if not found_duplicate_vote and user_extended_f != question.asked_by:
                current_date = datetime.datetime.now()
                vote = Vote.objects.create(voter=user_extended_f, vote_date=current_date, value=value, target=question)
                vote.save()
            return HttpResponseRedirect('/questions/' + question.id.__str__())
        elif answer_form.is_valid():
            current_date = datetime.datetime.now()
            answer_text = answer_form.cleaned_data['answer']
            answer = Answer.objects.create(
                published_by=user_extended_f, content=answer_text, pub_date=current_date, question=question, accepted=0
            )
            answer.save()
            return HttpResponseRedirect('/questions/' + question.id.__str__())
        elif question is not None:
            return HttpResponseRedirect('/accounts/login/?next=/questions/' + question.id.__str__())
        else:
            return HttpResponseRedirect('/404')
    return render(request, 'question_detail.html',
                  {'question': question, 'vote_sum': vote_sum, 'previous_vote': previous_vote})


def tag_page(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    questions = Question.objects.filter(tag=tag)
    return render(request, 'tag_page.html', {'tag': tag, 'questions': helper.default_questions_paginator(request, questions)})


def user_page(request, user_id):
    otheruser = get_object_or_404(UserExtended, pk=user_id)
    form = AnswerForm
    return render(request, 'user_page.html', {'otheruser': otheruser, 'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/index/')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register_form.html', {'form': form})


def new_question(request):
    if request.POST:
        form = NewQuestionForm(request.POST, user=UserExtended.objects.filter(user=request.user).first(), pub_date=datetime.datetime.now())
        form.save()
        return redirect('/users/' + request.user.id.__str__())
    else:
        form = NewQuestionForm(user=UserExtended.objects.filter(user=request.user).first(), pub_date=datetime.datetime.now())
    return render(request, 'new_question.html', {'form': form})


def search(request):
    if request.GET:
        phrase = request.GET.get("input_search_phrase")
        #matching_text = r'^*' + phrase + r'*'
        matching_text = phrase
        questions = Question.objects.filter(Q(title=matching_text) | Q(content=matching_text))
        return render(request, 'search_question.html', {'questions': helper.default_questions_paginator(request, questions), 'phrase': phrase})
    return render(request, 'index')