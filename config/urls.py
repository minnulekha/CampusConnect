from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('faculty/', include('faculty.urls', namespace='faculty')),
    path('location/', include('location.urls', namespace='location')),
    path('community/', include('community.urls', namespace='community')),
    path('appointments/', include('appointments.urls', namespace='appointments')),
    path('campus/', include('campus.urls', namespace='campus')), # <-- Add this line
    path('', lambda request: redirect('faculty:search')), 
]