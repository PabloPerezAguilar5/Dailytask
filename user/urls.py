from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'user'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.facial_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),  # Perfil propio
    path('profile/<str:username>/', views.profile, name='profile'),  # Perfil de otro usuario
    path('family/create/', views.create_family_group, name='create_family'),
] 