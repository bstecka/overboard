 # core/views.py
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.db.models import Count, Sum, Q
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.views import View
from .models import Question, Tag, Vote, Answer
from .forms import AnswerForm, VoteForm, AnswerVoteForm, RegistrationForm, NewQuestionForm
import datetime
#from django.views.generic import TemplateView
#from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.decorators import login_required


def tag_list(request):
    tags = Tag.objects.all().annotate(num_questions=Count('questions')).order_by('-num_questions')
    return render(request, 'tag/tags_list.html', {'tags': tags})


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


def new_answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user = request.user
    if request.POST:
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            current_date = datetime.datetime.now()
            answer_text = answer_form.cleaned_data['answer']
            answer = Answer.objects.create(
                published_by=user, content=answer_text, pub_date=current_date, question=question, accepted=0
            )
            answer.save()
    return HttpResponseRedirect(reverse('core:question_detail', args=(question.id,)))


def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user = request.user
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
        else:
            return HttpResponseRedirect('/404')
    return HttpResponseRedirect(reverse('core:question_detail', args=(question.id,)))


def answer_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user = request.user
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
    return HttpResponseRedirect(reverse('core:question_detail', args=(question.id,)))


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

    return render(request, 'question_page.html',
                  {'question': question, 'answersums': answer_sums, 'answervotes': answer_votes,
                   'vote_sum': vote_sum, 'previous_vote': previous_vote})


def tag_page(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    questions = Question.objects.filter(tag=tag)
    return render(request, 'tag/tag_page.html', {'tag': tag, 'questions': questions})


def user_page(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    form = AnswerForm
    return render(request, 'user_page.html', {'otheruser': other_user, 'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('core:index'))
    else:
        form = RegistrationForm()
    return render(request, 'registration/register_form.html', {'form': form})


def search(request):
    if request.GET:
        phrase = request.GET.get("input_search_phrase")
        questions = Question.objects.filter(Q(title__contains=phrase) | Q(content__contains=phrase))
        return render(request, 'search_question.html', {'questions': questions, 'phrase': phrase})
    return render(request, 'index')


class NewQuestionView(View):
    form_class = NewQuestionForm

    def post(self, request):
        form = self.form_class(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('users:user_page', args=(request.user.id,)))

    def get(self, request):
        return render(request, 'new_question.html', {'form': self.form_class()})


