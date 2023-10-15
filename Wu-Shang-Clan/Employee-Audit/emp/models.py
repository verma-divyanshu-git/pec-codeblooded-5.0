from django.db import models
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField


class Department(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Position(models.Model):
    title = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Employee(models.Model):
    name = models.CharField(max_length=200)
    emp_id = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=150)
    working = models.BooleanField(default=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)
    position = models.ForeignKey(
        Position, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='tasks')
    due_date = models.DateField()

    def __str__(self):
        return self.title


class AuditLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    # 'CREATE', 'READ', 'UPDATE', 'DELETE'
    action = models.CharField(max_length=10)
    # The model name (e.g., 'Employee')
    model = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField()  # ID of the affected object
    details = models.TextField()  # Additional details or changes


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class ProjectAssignment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class EmployeeSkill(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)


class Office(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class EmployeeOfficeAssignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)


auditlog.register(Department)
auditlog.register(Position)
auditlog.register(Employee)
auditlog.register(Task)
auditlog.register(AuditLog)
auditlog.register(Project)
auditlog.register(ProjectAssignment)
auditlog.register(Skill)
auditlog.register(EmployeeSkill)
auditlog.register(Office)
auditlog.register(EmployeeOfficeAssignment)
