from django.db import models
from accounts.models import FacultyProfile, Department

class Subject(models.Model):
    SEMESTER_CHOICES = [(i, f'Semester {i}') for i in range(1, 9)]
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    # Adding Department and Semester for filtering
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    semester = models.IntegerField(choices=SEMESTER_CHOICES, default=1)

    def __str__(self):
        dept_code = self.department.code if self.department else "GEN"
        return f"S{self.semester} {dept_code} - {self.name} ({self.code})"

class Timetable(models.Model):
    DAYS_OF_WEEK = (
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
    )
    
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='timetables')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50) # e.g., 'Room 204' or 'Lab 403'

    def __str__(self):
        return f"{self.faculty.user.last_name} - {self.subject.code} ({self.day})"