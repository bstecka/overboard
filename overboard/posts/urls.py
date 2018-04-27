from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

# from tags import urls

app_name = 'posts'
urlpatterns = [
    path('', views.QuestionList.as_view(selected_tab='last'), name='questions'),
    path('<int:question_id>/', views.question_detail, name='question_page'),
    path('new_question/', login_required(views.NewQuestionView.as_view()), name='new_question'),
    path('new_answer/<int:question_id>/', login_required(views.new_answer), name='new_answer'),
    path('answer_vote/<int:question_id>/', login_required(views.answer_vote), name='answer_vote'),
    path('question_vote/<int:question_id>/', login_required(views.question_vote), name='question_vote'),

    # path('search/', views.search, name='search'),
]