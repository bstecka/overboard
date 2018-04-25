from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
# from tags import urls

app_name = 'core'
urlpatterns = [
    path('', views.latest_question_list, name='index'),
    path('index/', views.latest_question_list, name='latest_question_list'),
    path('index/topweek/', views.top_week_questions, name='top_week_questions'),
    path('index/topmonth/', views.top_month_questions, name='top_month_questions'),
    path('search/', views.search, name='search'),

    path('questions/', views.latest_question_list, name='questions'),
    path('questions/<int:question_id>/', views.question_detail, name='question_detail'),
    path('new_question/', login_required(views.NewQuestionView.as_view()), name='new_question'),
    path('new_answer/<int:question_id>/', login_required(views.new_answer), name='new_answer'),
    path('answer_vote/<int:question_id>/', login_required(views.answer_vote), name='answer_vote'),
    path('question_vote/<int:question_id>/', login_required(views.question_vote), name='question_vote'),

    # path('users/', views.latest_question_list, name='users'),
    # path('users/<int:user_id>/', views.user_page, name='user_page'),
    # path('register/', views.register, name='register'),

    # path('tags/', views.tag_list, name='tag_list'),
    # path('tags/<int:tag_id>/', views.tag_page, name='tag_page'),
]
