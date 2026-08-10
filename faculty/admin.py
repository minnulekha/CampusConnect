from django.contrib import admin
from .models import Subject, Timetable

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    # Shows these columns in the subject list
    list_display = ('name', 'code', 'department', 'semester')
    # Adds a filter sidebar on the right side of the screen!
    list_filter = ('department', 'semester')
    # Allows typing to search for subjects
    search_fields = ('name', 'code')

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'subject', 'day', 'start_time', 'end_time', 'room')
    # Filter timetables easily by department, semester, and day
    list_filter = ('day', 'faculty', 'subject__department', 'subject__semester')
    
    # This creates a searchable dropdown for subjects instead of a massive scrolling list
    autocomplete_fields = ['subject']