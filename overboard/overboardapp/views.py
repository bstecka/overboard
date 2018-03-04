 # overboardapp/views.py
from django.shortcuts import render
from django.views.generic import TemplateView
from overboardapp.models import Notification
from django.http import HttpResponse

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
