 # overboardapp/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Notification
from .models import Question
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


def latest_question_list(request):
    latest_questions = Question.objects.all().order_by('-pub_date')[:10]
    return render(request, 'index_content.html', {'questions': latest_questions, 'selected_tab': 'last'});


def topweek_question_list(request):
    from_date = datetime.datetime.now() - datetime.timedelta(days=7)
    latest_questions = Question.objects.filter(pub_date__range=[from_date, datetime.datetime.now()]).order_by('-pub_date')[:10]
    return render(request, 'index_content.html', {'questions': latest_questions, 'selected_tab': 'week'});
