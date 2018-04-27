from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
# from core import urls

app_name = 'tags'
urlpatterns = [
    path('', views.TagList.as_view(), name='tag_list'),
    path('<int:pk>', views.TagDetailView.as_view(), name='tag_page'),
]
