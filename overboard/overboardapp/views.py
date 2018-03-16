 # overboardapp/views.py
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from django.db.models import Count
from .models import Notification, Question, Tag
from .forms import AnswerForm
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
    return render(request, 'index_content.html', {'questions': latest_questions, 'selected_tab': 'last'})


def topweek_question_list(request):
    from_date = datetime.datetime.now() - datetime.timedelta(days=7)
    latest_questions = Question.objects.filter(pub_date__range=[from_date, datetime.datetime.now()]).order_by('-pub_date')[:10]
    return render(request, 'index_content.html', {'questions': latest_questions, 'selected_tab': 'week'})


def question_detail(request, question_id):   # Page with details of question
    question = get_object_or_404(Question, pk=question_id)
    form = AnswerForm
    return render(request, 'question_detail.html', {'question': question, 'form': form})


def tag_page(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    questions = Question.objects.filter(tag=tag)
    return render(request, 'tag_page.html', {'tag': tag, 'questions': questions})

