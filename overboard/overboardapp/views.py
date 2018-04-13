 # overboardapp/views.py
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from .models import Notification, Question, Tag, Vote, UserExtended, Answer
from .forms import AnswerForm, VoteForm, AnswerVoteForm, RegistrationForm, NewQuestionForm
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


def new_answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user = request.user
    if not user.is_authenticated:  # na reverse'ie??????
        return HttpResponseRedirect('/accounts/login/?next=/questions/' + question.id.__str__())
    if request.POST:
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            current_date = datetime.datetime.now()
            answer_text = answer_form.cleaned_data['answer']
            answer = Answer.objects.create(
                published_by=user, content=answer_text, pub_date=current_date, question=question, accepted=0
            )
            answer.save()
    return HttpResponseRedirect('/questions/' + question.id.__str__())


def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user = request.user
    if not user.is_authenticated:  # na reverse'ie??????
        return HttpResponseRedirect('/accounts/login/?next=/questions/' + question.id.__str__())
    if request.POST:
        vote_form = VoteForm(request.POST)
        if vote_form.is_valid():
            value = vote_form.cleaned_data['vote']
            found_duplicate_vote = False
            found_opposite_vote = False
            found_vote = Vote.objects.first()
            for v in question.votes.all():
                if v.voter == user and v.value == value:
                    found_duplicate_vote = True
                    found_vote = v
                elif v.voter == user:
                    found_opposite_vote = True
                    found_vote = v
            if found_duplicate_vote or found_opposite_vote:
                found_vote.delete()
            if not found_duplicate_vote and user != question.asked_by:
                current_date = datetime.datetime.now()
                vote = Vote.objects.create(voter=user, vote_date=current_date, value=value, target=question)
                vote.save()
            return HttpResponseRedirect('/questions/' + question.id.__str__())
        else:
            return HttpResponseRedirect('/404')
    return HttpResponseRedirect('/questions/' + question.id.__str__())


def answer_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user = request.user
    if not user.is_authenticated:  # na reverse'ie??????
        return HttpResponseRedirect('/accounts/login/?next=/questions/' + question.id.__str__())
    if request.POST:
        answer_vote_form = AnswerVoteForm(request.POST)
        if answer_vote_form.is_valid():
            value = answer_vote_form.cleaned_data['vote']
            answer = Answer.objects.filter(id=answer_vote_form.cleaned_data['target']).first()
            found_duplicate_vote = False
            found_opposite_vote = False
            found_vote = Vote.objects.first()
            for v in answer.votes.all():
                if v.voter == user and v.value == value:
                    found_duplicate_vote = True
                    found_vote = v
                elif v.voter == user:
                    found_opposite_vote = True
                    found_vote = v
            if found_duplicate_vote or found_opposite_vote:
                found_vote.delete()
            if not found_duplicate_vote and user != answer.published_by:
                current_date = datetime.datetime.now()
                vote = Vote.objects.create(voter=user, vote_date=current_date, value=value, target=answer)
                vote.save()
            return HttpResponseRedirect('/questions/' + question.id.__str__())
    return HttpResponseRedirect('/questions/' + question.id.__str__())


def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    vote_sum = question.votes.all().aggregate(Sum('value'))
    previous_vote = 0
    user = User.objects.filter(username=request.user.get_username()).first()

    answers = Answer.objects.filter(question=question)
    answer_votes = {'answer_id': 0}
    answer_sums = {'answer_id': 0}
    for a in answers.all():
        answer_sums[a.id] = a.votes.aggregate(Sum('value'))
        for v in a.votes.all():
            if v.voter == user:
                answer_votes[a.id] = v.value

    for v in question.votes.all():
        if v.voter == user:
            previous_vote = v.value

    return render(request, 'question_detail.html',
                  {'question': question, 'answersums': answer_sums, 'answervotes': answer_votes,
                   'vote_sum': vote_sum, 'previous_vote': previous_vote})


def tag_page(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    questions = Question.objects.filter(tag=tag)
    return render(request, 'tag_page.html', {'tag': tag, 'questions': helper.default_questions_paginator(request, questions)})


def user_page(request, user_id):
    otheruser = get_object_or_404(User, pk=user_id)
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
        form = NewQuestionForm(request.POST, user=request.user, pub_date=datetime.datetime.now())
        form.save()
        return redirect('/users/' + request.user.id.__str__())
    else:
        form = NewQuestionForm(user=request.user, pub_date=datetime.datetime.now())
    return render(request, 'new_question.html', {'form': form})


def search(request):
    if request.GET:
        phrase = request.GET.get("input_search_phrase")
        questions = Question.objects.filter(Q(title__contains=phrase) | Q(content__contains=phrase))
        return render(request, 'search_question.html', {'questions': helper.default_questions_paginator(request, questions), 'phrase': phrase})
    return render(request, 'index')