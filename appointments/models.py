from django.db import models
from django.conf import settings
from accounts.models import FacultyProfile

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments_as_student')
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='appointments')
    
    purpose = models.CharField(max_length=150)
    date = models.DateField()
    preferred_time = models.TimeField()
    message = models.TextField(blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} with Dr. {self.faculty.user.last_name} on {self.date}"