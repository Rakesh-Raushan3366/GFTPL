from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Sum
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import csv

from .models import Department, Employee, Project
from .serializers import DepartmentSerializer, EmployeeSerializer, ProjectSerializer
from .permissions import ReadOnlyOrAdminManager


# -------------------- Department APIs --------------------

@api_view(["GET"])
@permission_classes([ReadOnlyOrAdminManager])
def list_departments(request):
    """Get all departments with employee count"""
    try:
        departments = Department.objects.all().annotate(employee_count=Count('employees'))
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def export_departments_csv(request):
    """Export departments as CSV"""
    try:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="departments.csv"'

        writer = csv.writer(response)
        writer.writerow(["ID", "Name", "Description", "Employee Count"])

        for d in Department.objects.all().annotate(employee_count=Count('employees')):
            writer.writerow([d.id, d.name, d.description, d.employee_count])

        return response
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# -------------------- Employee APIs --------------------

@api_view(["GET"])
@permission_classes([ReadOnlyOrAdminManager])
def list_employees(request):
    """Get all employees"""
    try:
        employees = Employee.objects.select_related("department").all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def employees_by_department(request):
    """Report: employee count per department"""
    try:
        data = (
            Employee.objects.values("department__id", "department__name")
            .annotate(count=Count("id"))
            .order_by("department__name")
        )
        return Response(list(data))
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def salary_per_department(request):
    """Report: total salary per department"""
    try:
        data = (
            Employee.objects.values("department__id", "department__name")
            .annotate(total_salary=Sum("salary"))
            .order_by("department__name")
        )
        return Response(list(data))
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def export_employees_csv(request):
    """Export employees as CSV"""
    try:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="employees.csv"'

        writer = csv.writer(response)
        writer.writerow(["ID", "Full Name", "Email", "Department", "Salary", "Active"])

        for e in Employee.objects.select_related("department").all():
            writer.writerow([e.id, e.full_name, e.email, e.department.name, e.salary, e.active])

        return response
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# -------------------- Project APIs --------------------

@api_view(["GET"])
@permission_classes([ReadOnlyOrAdminManager])
def list_projects(request):
    """Get all projects"""
    try:
        projects = Project.objects.select_related("department").prefetch_related("employees").all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def active_projects(request):
    """Get active projects"""
    try:
        projects = Project.objects.filter(active=True)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def export_projects_csv(request):
    """Export projects as CSV"""
    try:
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="projects.csv"'

        writer = csv.writer(response)
        writer.writerow(["ID", "Name", "Description", "Department", "Active"])

        for p in Project.objects.select_related("department").all():
            writer.writerow([p.id, p.name, p.description, p.department.name, p.active])

        return response
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
