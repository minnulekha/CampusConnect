from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('book/<int:faculty_id>/', views.book_appointment, name='book'),
    path('update/<int:appointment_id>/', views.update_appointment_status, name='update_status'),
]