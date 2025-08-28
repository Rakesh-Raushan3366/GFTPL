from django.contrib import admin
from .models import *

# Register your models here.

# -------------------- User Table Register And Also Adding display, Filter, Search --------------------
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email')

# -------------------- Department Table Register And Also Adding display, Search --------------------
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# -------------------- Employee Table Register And Also Adding display, Filter, Search --------------------
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'department', 'salary', 'active')
    list_filter = ('department', 'active')
    search_fields = ('full_name', 'email')

# -------------------- Project Table Register And Also Adding display, Filter, Search --------------------
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'department', 'start_date', 'end_date', 'active')
    list_filter = ('department', 'active')
    search_fields = ('name',)