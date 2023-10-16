from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("home/", emp_home),
    path("department-list/", department_list),
    # path("update-department/", update_department),
    # path("delete-department/", delete_department),
    path('delete-emp/<int:emp_id>/', delete_employee, name='delete_employee'),
    path("update-emp/<int:emp_id>", update_emp),
    path("do-update-emp/<int:emp_id>", do_update_emp),
    path('add-department/', add_department),
    path("add_employee/", add_employee),
    # path("delete-emp/<int:emp_id>", delete_employee),
    # path("update-emp/<int:emp_id>", update_emp),
    # path("do-update-emp/<int:emp_id>", do_update_emp),
    # path('add-department/', add_department),
    path('add-task/', add_task),
    path('add-skill/', add_skill),
    path('add-office/', add_office),
    path('add-project-assignment/', add_project_assignment),
    path('add-employee-skill/', add_employee_skill),
    path('add-employee-office-assignment/', add_employee_office_assignment),
    path('add-position/', add_position),
]
