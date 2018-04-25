from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
# from core import urls

app_name = 'tags'
urlpatterns = [
    path('', views.tag_list, name='tag_list'),
    path('<int:tag_id>/', views.tag_page, name='tag_page'),
]
