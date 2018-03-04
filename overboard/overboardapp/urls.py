from django.conf.urls import url
from django.contrib import admin
from overboardapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.HomePageView.as_view()),
    url(r'^page/$', views.PageView.as_view()),
]
