from django.urls import path
from . import views


urlpatterns = [
    # ---------------- Departments ----------------
    path("departments/", views.list_departments, name="list_departments"),
    path("departments/export/", views.export_departments_csv, name="export_departments"),

    # ---------------- Employees ----------------
    path("employees/", views.list_employees, name="list_employees"),
    path("employees/by-department/", views.employees_by_department, name="employees_by_department"),
    path("employees/salary-report/", views.salary_per_department, name="salary_per_department"),
    path("employees/export/", views.export_employees_csv, name="export_employees"),

    # ---------------- Projects ----------------
    path("projects/", views.list_projects, name="list_projects"),
    path("projects/active/", views.active_projects, name="active_projects"),
    path("projects/export/", views.export_projects_csv, name="export_projects"),
]
