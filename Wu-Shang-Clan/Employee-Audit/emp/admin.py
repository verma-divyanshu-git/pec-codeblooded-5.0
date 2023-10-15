from django.contrib import admin
from django.contrib import admin
from .models import Employee, Department, Task, Skill, Office, ProjectAssignment, EmployeeSkill, EmployeeOfficeAssignment, Position, AuditLog

# Register your models here.
admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Task)
admin.site.register(Skill)
admin.site.register(Office)
admin.site.register(ProjectAssignment)
admin.site.register(EmployeeSkill)
admin.site.register(EmployeeOfficeAssignment)
admin.site.register(Position)
admin.site.register(AuditLog)
