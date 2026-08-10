from django.urls import path
from . import views

app_name = 'location'

urlpatterns = [
    path('scan/<slug:slug>/', views.scan_checkin, name='qr_checkin'),
    path('dashboard/', views.faculty_dashboard, name='dashboard'), # <-- Add this line
    path('update-gps/', views.update_gps, name='update_gps'),      # <-- Add this line
]