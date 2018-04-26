from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.db.models import Count, Sum, Q
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth import login, authenticate
import datetime

from .models import Question, Tag, Vote, Answer
from .forms import RegistrationForm, AnswerForm

# Create your views here.

def latest_question_list(request):
    latest_questions = Question.objects.all().order_by('-pub_date')
    return render(request, 'index_content.html', {'questions': latest_questions, 'selected_tab': 'last'})


def user_page(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    form = AnswerForm
    return render(request, 'user_page.html', {'otheruser': other_user, 'form': form })


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
    return render(request, 'register_form.html', {'form': form})