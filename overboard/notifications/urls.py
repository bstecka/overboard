from django.urls import path
from . import views

app_name = 'notifications'
urlpatterns = [
    path('visited/<int:pk>/', views.notification_visited, name='notification_visited'),
    path('delete/<int:pk>/', views.delete, name='delete'),
]