from django.urls import path
from . import views

# App namespace mapping
app_name = 'faculty'

urlpatterns = [
    path('', views.faculty_search, name='search'),
    path('profile/<int:pk>/', views.faculty_profile, name='profile'),
]