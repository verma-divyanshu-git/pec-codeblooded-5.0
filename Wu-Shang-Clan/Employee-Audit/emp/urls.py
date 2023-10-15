from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path("home/", emp_home),
    path("add_employee/", add_employee),
    path("delete-emp/<int:emp_id>", delete_employee),
    path("update-emp/<int:emp_id>", update_emp),
    path("do-update-emp/<int:emp_id>", do_update_emp),
    path('add-department/', add_department)
]
