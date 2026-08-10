from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return self.username

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class QRLocation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=100, unique=True) 
    
    # New GPS mapping fields for proximity checking
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - Student"

class FacultyProfile(models.Model):
    AVAILABILITY_CHOICES = (
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('in_class', 'In Class'),
        ('in_meeting', 'In Meeting'),
        ('away', 'Away'),
        ('offline', 'Offline'),
    )
    LOCATION_SOURCE_CHOICES = (
        ('gps', '🟢 Live GPS'),
        ('qr', '🔵 Faculty QR Scanner'),
        ('timetable', '🟡 Expected from Timetable'),
        ('report', '🟠 Student Reported'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='faculty_profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    designation = models.CharField(max_length=100, blank=True)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='offline')
    
    current_location_string = models.CharField(max_length=200, default="Unknown")
    location_source = models.CharField(max_length=20, choices=LOCATION_SOURCE_CHOICES, default='timetable')
    location_updated_at = models.DateTimeField(auto_now=True)
    
    # New raw tracking coordinate metrics
    current_latitude = models.FloatField(null=True, blank=True)
    current_longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Dr/Prof {self.user.first_name} {self.user.last_name}"