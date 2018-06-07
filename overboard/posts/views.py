from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.db.models import Count, Sum, Q
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.views import View
from hitcount.views import HitCountDetailView
from tags.models import Tag
from notifications.models import UserNotification
from .models import Question, Vote, Answer
from .forms import AnswerForm, VoteForm, AnswerVoteForm, NewQuestionForm
import datetime
# Create your views here.

num_of_votes_popular_question_not = 0
num_of_votes_popular_answer_not = 0

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


''' not yet used in app posts. currently this option is in core app'''
# class TopQuestionList(QuestionList):
#     delta_time = 0
#
#     def get_queryset(self):
#         from_date = datetime.datetime.now() - datetime.timedelta(days=self.delta_time)
#         questions = Question.objects.filter(pub_date__range=[from_date, datetime.datetime.now()]).annotate(
#             number_of_votes=Count('votes'))
#         return questions.order_by('-number_of_votes')



''' old views'''

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


class NewQuestionView(View):
    form_class = NewQuestionForm

    def post(self, request):
        form = self.form_class(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('users:user_page', args=(request.user.id,)))

    def get(self, request):
        return render(request, 'new_question.html', {'form': self.form_class()})


class QuestionCreateView(CreateView):
    model = Question
    fields = ['title', 'content']
    template_name = 'new_question.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(QuestionCreateView, self).form_valid(form)


def new_answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user = request.user
    if request.POST:
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            current_date = datetime.datetime.now()
            answer_text = answer_form.cleaned_data['answer']
            answer = Answer.objects.create(published_by=user, content=answer_text, pub_date=current_date, question=question, accepted=0)
            answer.save()
            notification = UserNotification.objects.create_notification_for_new_answer(answer)
            notification.save()
    return HttpResponseRedirect(reverse('posts:question_page', args=(question.id,)))


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
                if value == 1 and question.all_vote_set.filter(value=1).count() > num_of_votes_popular_answer_not:
                    UserNotification.objects.create_notification_for_popular_question(question).save()
    return HttpResponseRedirect(reverse('posts:question_page', args=(question.id,)))


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
                if value == 1 and question.all_vote_set.filter(value=1).count() > num_of_votes_popular_answer_not:
                    UserNotification.objects.create_notification_for_popular_answer(answer).save()
    return HttpResponseRedirect(reverse('posts:question_page', args=(question.id,)))


class QuestionView(HitCountDetailView):
    model = Question
    context_object_name = 'question'
    template_name = 'question_page.html'
    count_hit = True


    def get_context_data(self, **kwargs):
        context = super(QuestionView, self).get_context_data(**kwargs)
        question = self.object
        user = User.objects.filter(username=self.request.user.get_username()).first()
        answers = Answer.objects.filter(question=question)

        answer_votes = {'answer_id': 0}
        answer_sums = {'answer_id': 0}
        for a in answers.all():
            answer_sums[a.id] = a.votes.aggregate(Sum('value'))
            for v in a.votes.all():
                if v.voter == user:
                    answer_votes[a.id] = v.value

        previous_vote = 0
        for v in question.votes.all():
            if v.voter == user:
                previous_vote = v.value

        context['answersums'] = answer_sums
        context['answervotes'] = answer_votes
        context['vote_sum'] = question.votes.all().aggregate(Sum('value'))
        context['previous_vote'] = previous_vote
        return context