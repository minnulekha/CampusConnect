from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Department, StudentProfile, FacultyProfile, QRLocation

# Customize the UserAdmin class to expose the new custom role field
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Roles', {'fields': ('role',)}),
    )

# Register CustomUser with our updated admin configurations
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Department)
admin.site.register(StudentProfile)
admin.site.register(FacultyProfile)

@admin.register(QRLocation)
class QRLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'slug')
    prepopulated_fields = {'slug': ('name',)}