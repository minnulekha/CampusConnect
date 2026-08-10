from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('ask/<int:faculty_id>/', views.ask_location, name='ask'),
    path('reply/<int:question_id>/', views.reply_location, name='reply'),
    path('notifications/', views.view_notifications, name='notifications'),
]