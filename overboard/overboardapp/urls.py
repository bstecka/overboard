from django.conf.urls import url
from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', views.latest_question_list, name='latest_question_list'),
    url(r'^index/topweek/$', views.topweek_question_list, name='topweek_question_list'),
    url(r'^page/$', views.PageView.as_view()),
    url(r'^questions/$', views.latest_question_list, name='questions'),
    path('questions/<int:question_id>/', views.question_detail, name='question_detail'),
    url(r'^users/$', views.latest_question_list, name='users'),
    path('', views.latest_question_list, name='latest_question_list'),
]
