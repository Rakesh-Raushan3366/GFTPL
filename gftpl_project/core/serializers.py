from rest_framework import serializers
from .models import *

# Create your serializers here.

# -------------------- Department JSON --------------------
class DepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'employee_count']

# -------------------- Employees JSON --------------------
class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.ReadOnlyField(source='department.name')

    class Meta:
        model = Employee
        fields = ['id', 'full_name', 'email', 'department', 'department_name', 'salary', 'date_joined', 'active', 'user']
        read_only_fields =['date_joined']

# -------------------- Project JSON --------------------
class ProjectSerializer(serializers.ModelSerializer):
    department_name = serializers.ReadOnlyField(source='department.name')
    employee_ids = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), many=True, source='employee', required=False)

    class Meta:
        model =Project
        fields = ['id', 'name', 'description', 'department', 'department_name', 'start_date', 'end_date', 'active', 'employee_ids']