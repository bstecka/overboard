from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.db.models import Count, Sum, Q
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.views import View
from .models import Question, Vote, Answer
from tags.models import Tag
from users.models import UserExtended
from .forms import AnswerForm, VoteForm, AnswerVoteForm, NewQuestionForm
import datetime
# Create your views here.


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
    form_class = NewQuestionForm()

    def post(self, request):
        form = NewQuestionForm(request.POST)
        form.save()
        return HttpResponseRedirect(reverse('users:user_page', args=(request.user.id,)))

    def get(self, request):
        user = UserExtended.objects.filter(user=self.request.user).first()
        return render(request, 'new_question.html', {'form': NewQuestionForm(user=user)})



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
            answer = Answer.objects.create(
                published_by=user, content=answer_text, pub_date=current_date, question=question, accepted=0
            )
            answer.save()
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
            voter = UserExtended.objects.filter(user=user).first()
            if found_duplicate_vote or found_opposite_vote:
                if not (voter.reputation < 10 and value < 0):
                    found_vote.delete()
                    vote_target_user = UserExtended.objects.filter(user=question.asked_by).first()
                    vote_target_user.reputation = vote_target_user.reputation - found_vote.value
                    vote_target_user.save()
            if not found_duplicate_vote and user != question.asked_by:
                current_date = datetime.datetime.now()
                if not (voter.reputation < 10 and value < 0):
                    vote = Vote.objects.create(voter=user, vote_date=current_date, value=value, target=question)
                    vote.save()
                    vote_target_user = UserExtended.objects.filter(user=question.asked_by).first()
                    vote_target_user.reputation = vote_target_user.reputation + value
                    vote_target_user.save()
        else:
            return HttpResponseRedirect('/404')
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
            voter = UserExtended.objects.filter(user=user).first()
            if found_duplicate_vote or found_opposite_vote:
                if not (voter.reputation < 10 and value < 0):
                    found_vote.delete()
                    vote_target_user = UserExtended.objects.filter(user=answer.published_by).first()
                    vote_target_user.reputation = vote_target_user.reputation - found_vote.value
                    vote_target_user.save()
            if not found_duplicate_vote and user != answer.published_by:
                if not (voter.reputation < 10 and value < 0):
                    current_date = datetime.datetime.now()
                    vote = Vote.objects.create(voter=user, vote_date=current_date, value=value, target=answer)
                    vote.save()
                    vote_target_user = UserExtended.objects.filter(user=answer.published_by).first()
                    vote_target_user.reputation = vote_target_user.reputation + value
                    vote_target_user.save()
    return HttpResponseRedirect(reverse('posts:question_page', args=(question.id,)))


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
