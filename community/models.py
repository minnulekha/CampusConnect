from django.db import models
from django.conf import settings
from accounts.models import FacultyProfile

class LocationQuestion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions')
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='location_questions')
    text = models.CharField(max_length=255, default="Where is this faculty member right now?")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query about Dr. {self.faculty.user.last_name} by {self.user.username}"

class LocationReply(models.Model):
    question = models.ForeignKey(LocationQuestion, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    info_source = models.CharField(max_length=200) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.username}"

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.user.username}"