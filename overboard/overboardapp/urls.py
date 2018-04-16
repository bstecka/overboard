from django.conf.urls import url
from django.contrib import admin
from . import views
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('', views.latest_question_list, name='latest_question_list'),
    url(r'^index/$', views.latest_question_list, name='latest_question_list'),
    url(r'^index/topweek/$', views.topweek_question_list, name='topweek_question_list'),
    url(r'^search/$', views.search, name='search'),

    url(r'^tags/$', views.tag_list, name='tag_list'),
    path('tags/<int:tag_id>/', views.tag_page, name='tag_page'),

    url(r'^questions/$', views.latest_question_list, name='questions'),
    path('questions/<int:question_id>/', views.question_detail, name='question_detail'),
    url(r'^new_question/$', login_required(views.NewQuestionView.as_view()), name='new_question'),
    path('new_answer/<int:question_id>/', views.new_answer, name='new_answer'),
    path('answer_vote/<int:question_id>/', views.answer_vote, name='answer_vote'),
    path('question_vote/<int:question_id>/', views.question_vote, name='question_vote'),

    url(r'^users/$', views.latest_question_list, name='users'),
    path('users/<int:user_id>/', views.user_page, name='user_page'),
    url(r'^register/$', views.register, name='register'),


    url(r'^page/$', views.PageView.as_view(), name='page'),
]
