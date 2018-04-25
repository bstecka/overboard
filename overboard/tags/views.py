from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Q
from django.views import View
from .models import Question, Tag, Vote, Answer
# from .forms import AnswerForm, VoteForm, AnswerVoteForm, RegistrationForm, NewQuestionForm
import datetime


# Create your views here.

def tag_list(request):
    tags = Tag.objects.all().annotate(num_questions=Count('questions')).order_by('-num_questions')
    return render(request, 'tags_list.html', {'tags': tags})

def tag_page(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    questions = Question.objects.filter(tag=tag)
    return render(request, 'tag_page.html', {'tag': tag, 'questions': questions})
