from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', views.latest_question_list, name='latest_question_list'),
    url(r'^index/topweek/$', views.topweek_question_list, name='topweek_question_list'),
    url(r'^page/$', views.PageView.as_view()),
    url(r'^questions/$', views.latest_question_list, name='questions'),
    url(r'^users/$', views.latest_question_list, name='users'),
]
