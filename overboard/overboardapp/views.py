 # overboardapp/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Notification
from .models import Question


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
    return render(request, 'index_content.html', {'latest_questions': latest_questions});


def topweek_question_list(request):
    latest_questions = Question.objects.all().order_by('-pub_date')[:10]
    return render(request, 'index_content.html', {'latest_questions': latest_questions});
