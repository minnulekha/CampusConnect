from django.shortcuts import render, get_object_or_404
from django.db import models
from accounts.models import FacultyProfile, Department
from community.views import generate_faculty_summary # <-- Add this import

def faculty_search(request):
    query = request.GET.get('q', '')
    dept_id = request.GET.get('department', '')
    status = request.GET.get('status', '')

    # Fetch all faculty profiles to start
    faculty_list = FacultyProfile.objects.select_related('user', 'department').all()

    # Filter by name (first name, last name, or username)
    if query:
        faculty_list = faculty_list.filter(
            models.Q(user__first_name__icontains=query) |
            models.Q(user__last_name__icontains=query) |
            models.Q(user__username__icontains=query)
        )

    # Filter by Department
    if dept_id:
        faculty_list = faculty_list.filter(department_id=dept_id)

    # Filter by Availability
    if status:
        faculty_list = faculty_list.filter(availability=status)

    departments = Department.objects.all()

    context = {
        'faculty_list': faculty_list,
        'departments': departments,
        'query': query,
        'selected_dept': dept_id,
        'selected_status': status,
    }
    return render(request, 'faculty/search.html', context)

def faculty_profile(request, pk):
    profile = get_object_or_404(FacultyProfile.objects.select_related('user', 'department'), pk=pk)
    
    # Fetch timetable sorted by day and time
    timetables = profile.timetables.all().select_related('subject').order_by('day', 'start_time')
    ai_summary = generate_faculty_summary(profile)
    context = {
        'profile': profile,
        'timetables': timetables,
        'ai_summary': ai_summary, # <-- Pass it to the template
    }
    return render(request, 'faculty/profile.html', context)