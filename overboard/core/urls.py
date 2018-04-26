from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.latest_question_list, name='index'),
    path('index/', views.latest_question_list, name='latest_question_list'),
    path('index/topweek/', views.top_week_questions, name='top_week_questions'),
    path('index/topmonth/', views.top_month_questions, name='top_month_questions'),
    path('search/', views.search, name='search'),
]
