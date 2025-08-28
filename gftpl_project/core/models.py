from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# -------------------- Custom Auth With Roles Dropdown --------------------
class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        MANAGER = 'MANAGER', 'Manager'
        EMPLOYEE = 'EMPLOYEE', 'Employee'

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.EMPLOYEE)

    def is_admin(self):
        return self.role == self.Roles.ADMIN or self.is_superuser

    def is_manager(self):
        return self.role == self.Roles.MANAGER

# -------------------- Department Table And Structure --------------------
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# -------------------- Employee Table And Structure With Map user and department --------------------
class Employee(models.Model):
    user = models.OneToOneField('core.User', on_delete=models.CASCADE, related_name='employee_profile', null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='employees')
    salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_joined = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name


# -------------------- Project Table And Structure With Map department And employee  --------------------
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='projects')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    employees = models.ManyToManyField(Employee, related_name='projects', blank=True)

    class Meta:
        unique_together = [('name', 'department')]

    def __str__(self):
        return self.name