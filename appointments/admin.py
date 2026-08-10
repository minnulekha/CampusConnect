from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'faculty', 'date', 'preferred_time', 'status')
    list_filter = ('status', 'date', 'faculty')