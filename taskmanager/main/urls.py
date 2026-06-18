from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView  # ← ДОБАВЛЕНО
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('diary/', views.diary, name='diary'),
    path('add/', views.add_record, name='add_record'),
    path('edit/<int:pk>/', views.edit_record, name='edit_record'),
    path('delete/<int:pk>/', views.delete_record, name='delete_record'),
    path('analytics/', views.analytics, name='analytics'),
]