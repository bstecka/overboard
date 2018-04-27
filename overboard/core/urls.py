from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.QuestionList.as_view(selected_tab='last'), name='index'),
    path('questions/', views.QuestionList.as_view(selected_tab='last'), name='questions'),
    path('index/', views.QuestionList.as_view(selected_tab='last'), name='latest_question_list'),
    path('index/topweek/', views.TopQuestionList.as_view(selected_tab='week', delta_time=7), name='top_week_questions'),
    path('index/topmonth/', views.TopQuestionList.as_view(selected_tab='month', delta_time=30), name='top_month_questions'),
    path('search/', views.search, name='search'),
]
