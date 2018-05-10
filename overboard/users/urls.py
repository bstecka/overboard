from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views


app_name = 'users'
urlpatterns = [
    path('', views.QuestionList.as_view(selected_tab='last'), name='users'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user_page'),
    path('register/', views.register, name='register'),
]