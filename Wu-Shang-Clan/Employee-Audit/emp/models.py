from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models


class Emp(models.Model):
    name = models.CharField(max_length=200)
    emp_id = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=150)
    working = models.BooleanField(default=True)
    department = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(
        Emp, on_delete=models.CASCADE, related_name='tasks')
    due_date = models.DateField()

    def __str__(self):
        return self.title


class CRUDLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    # 'CREATE', 'READ', 'UPDATE', 'DELETE'
    action = models.CharField(max_length=10)
    # The model name (e.g., 'Employee')
    model = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField()  # ID of the affected object
    details = models.TextField()  # Additional details or changes
