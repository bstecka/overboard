from django.conf.urls import url
from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', views.latest_question_list, name='latest_question_list'),
    url(r'^index/topweek/$', views.topweek_question_list, name='topweek_question_list'),
    url(r'^tags/$', views.tag_list, name='tag_list'),
    url(r'^page/$', views.PageView.as_view(), name='page'),
    url(r'^questions/$', views.latest_question_list, name='questions'),
    path('tags/<int:tag_id>/', views.tag_page, name='tag_page'),
    path('questions/<int:question_id>/', views.question_detail, name='question_detail'),
    path('new_answer/<int:question_id>/', views.new_answer, name='new_answer'),
    path('answer_vote/<int:question_id>/', views.answer_vote, name='answer_vote'),
    path('question_vote/<int:question_id>/', views.question_vote, name='question_vote'),
    url(r'^users/$', views.latest_question_list, name='users'),
    path('users/<int:user_id>/', views.user_page, name='user_page'),
    path('', views.latest_question_list, name='latest_question_list'),
    url(r'^register/$', views.register, name='register'),
    url(r'^newquestion/$', views.new_question, name='new_question'),

]
