from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views


app_name = 'users'
urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('', views.latest_question_list, name='users'),
    path('<int:user_id>/', views.user_page, name='user_page'),
    path('register/', views.register, name='register'),
]