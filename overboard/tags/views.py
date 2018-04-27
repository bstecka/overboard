from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Q
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Question, Tag, Vote, Answer
import datetime


class TagList(ListView):
    model = Tag
    context_object_name = 'tags'
    template_name = 'tags_list.html'
    queryset = Tag.objects.all().annotate(num_questions=Count('questions')).order_by('-num_questions')


class TagDetailView(DetailView):
    model = Tag
    context_object_name = 'tag'
    template_name = 'tag_page.html'

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(tag=self.get_object())
        return context

