import math
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import QRLocation, FacultyProfile

@login_required
def scan_checkin(request, slug):
    qr_spot = get_object_or_404(QRLocation, slug=slug)
    if request.user.role != 'faculty':
        messages.error(request, "Access denied. Only faculty members can update location metrics.")
        return redirect('faculty:search')
        
    faculty_profile = request.user.faculty_profile
    faculty_profile.current_location_string = qr_spot.name
    faculty_profile.location_source = 'qr'
    faculty_profile.availability = 'available'
    faculty_profile.save()
    
    return render(request, 'location/success.html', {'room_name': qr_spot.name, 'description': qr_spot.description})

@login_required
def faculty_dashboard(request):
    if request.user.role != 'faculty':
        messages.error(request, "Access denied. Student portal routing is restricted.")
        return redirect('faculty:search')
        
    profile = request.user.faculty_profile
    
    if request.method == "POST":
        status = request.POST.get('availability', '')
        if status in dict(profile.AVAILABILITY_CHOICES):
            profile.availability = status
            profile.save()
            messages.success(request, f"Status set to {profile.get_availability_display()} successfully.")
            
    return render(request, 'location/dashboard.html', {'profile': profile})

@login_required
@csrf_exempt
def update_gps(request):
    if request.method == "POST" and request.user.role == 'faculty':
        import json
        data = json.loads(request.body)
        lat = data.get('latitude')
        lng = data.get('longitude')
        
        profile = request.user.faculty_profile
        profile.current_latitude = lat
        profile.current_longitude = lng
        profile.location_source = 'gps'
        
        # Super simple bounding box proximity calculation to find closest landmark room
        closest_location = "Academic Main Building"
        min_distance = float('inf')
        
        for spot in QRLocation.objects.exclude(latitude__isnull=True):
            # Distance approximation rule
            dist = math.sqrt((spot.latitude - lat)**2 + (spot.longitude - lng)**2)
            if dist < min_distance:
                min_distance = dist
                closest_location = f"Near {spot.name}"
        
        profile.current_location_string = closest_location
        profile.save()
        return JsonResponse({"status": "success", "resolved_location": closest_location})
        
    return JsonResponse({"status": "failed"}, status=400)