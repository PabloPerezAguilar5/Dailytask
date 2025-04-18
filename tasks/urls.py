from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.task_list, name='list'),
    path('create/', views.create_task, name='create'),
    path('<int:task_id>/complete/', views.complete_task, name='complete'),
    path('<int:task_id>/', views.task_detail, name='detail'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
] 