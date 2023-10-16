from django.db import models
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField
from auditlog.models import LogEntry


class Department(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    history_dep = AuditlogHistoryField()

    def __str__(self):
        return self.name


class Position(models.Model):
    title = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    history_pos = AuditlogHistoryField()

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
    history_employee = AuditlogHistoryField()

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='tasks')
    due_date = models.DateField()
    history_task = AuditlogHistoryField()

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
    history_proj = AuditlogHistoryField()

    def __str__(self):
        return self.name


class ProjectAssignment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    history_proj_ass = AuditlogHistoryField()


class Skill(models.Model):
    name = models.CharField(max_length=100)
    history_skill = AuditlogHistoryField()

    def __str__(self):
        return self.name


class EmployeeSkill(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    history_emp_skill = AuditlogHistoryField()


class Office(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    history_office = AuditlogHistoryField()

    def __str__(self):
        return self.name


class EmployeeOfficeAssignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    history_emp_office = AuditlogHistoryField()


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


# Copied Models:

class CopiedDepartment(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def _str_(self):
        return f"{self.name} (Copied)"


class CopiedPosition(models.Model):
    title = models.CharField(max_length=200)
    department = models.ForeignKey(CopiedDepartment, on_delete=models.CASCADE)

    def _str_(self):
        return f"{self.title} (Copied)"


class CopiedEmployee(models.Model):
    name = models.CharField(max_length=200)
    emp_id = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=150)
    working = models.BooleanField(default=True)
    department = models.ForeignKey(
        CopiedDepartment, on_delete=models.SET_NULL, null=True)
    position = models.ForeignKey(
        CopiedPosition, on_delete=models.SET_NULL, null=True)

    def _str_(self):
        return f"{self.name} (Copied)"


class CopiedTask(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(
        CopiedEmployee, on_delete=models.CASCADE, related_name='tasks')
    due_date = models.DateField()

    def _str_(self):
        return f"{self.title} (Copied)"


class CopiedAuditLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=10)
    model = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField()
    details = models.TextField()


class CopiedProject(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def _str_(self):
        return f"{self.name} (Copied)"


class CopiedProjectAssignment(models.Model):
    project = models.ForeignKey(CopiedProject, on_delete=models.CASCADE)
    employee = models.ForeignKey(CopiedEmployee, on_delete=models.CASCADE)


class CopiedSkill(models.Model):
    name = models.CharField(max_length=100)

    def _str_(self):
        return f"{self.name} (Copied)"


class CopiedEmployeeSkill(models.Model):
    employee = models.ForeignKey(CopiedEmployee, on_delete=models.CASCADE)
    skill = models.ForeignKey(CopiedSkill, on_delete=models.CASCADE)


class CopiedOffice(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)

    def _str_(self):
        return f"{self.name} (Copied)"


class CopiedEmployeeOfficeAssignment(models.Model):
    employee = models.ForeignKey(CopiedEmployee, on_delete=models.CASCADE)
    office = models.ForeignKey(CopiedOffice, on_delete=models.CASCADE)
