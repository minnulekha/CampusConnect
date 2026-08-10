from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import FacultyProfile
from .models import Appointment
from community.models import Notification

@login_required
def book_appointment(request, faculty_id):
    faculty = get_object_or_404(FacultyProfile, id=faculty_id)
    
    if request.method == "POST":
        purpose = request.POST.get('purpose', '').strip()
        date = request.POST.get('date', '')
        time = request.POST.get('time', '')
        message = request.POST.get('message', '').strip()
        
        if purpose and date and time:
            Appointment.objects.create(
                student=request.user,
                faculty=faculty,
                purpose=purpose,
                date=date,
                preferred_time=time,
                message=message
            )
            
            # Send notification to the faculty member
            Notification.objects.create(
                user=faculty.user,
                message=f"New appointment request submitted by student @{request.user.username}."
            )
            
            messages.success(request, "Appointment requested successfully! Awaiting faculty response.")
            
    return redirect('faculty:profile', pk=faculty_id)

@login_required
def update_appointment_status(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Security barrier: Only the specific faculty member can alter this status
    if request.user.role != 'faculty' or appointment.faculty != request.user.faculty_profile:
        messages.error(request, "Unauthorized action mapping configuration blocked.")
        return redirect('faculty:search')
        
    if request.method == "POST":
        new_status = request.POST.get('status', '')
        if new_status in ['accepted', 'rejected', 'completed']:
            appointment.status = new_status
            appointment.save()
            
            # Send alert ping back to the requesting student
            Notification.objects.create(
                user=appointment.student,
                message=f"Your appointment request with Dr. {appointment.faculty.user.last_name} has been {new_status}."
            )
            
            messages.success(request, f"Appointment status changed to {new_status.capitalize()}.")
            
    return redirect('location:dashboard')