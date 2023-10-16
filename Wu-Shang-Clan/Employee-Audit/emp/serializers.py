from rest_framework import serializers
from .models import AuditLog  # Import your AuditLog model
from auditlog.models import AuditlogHistoryField

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditlogHistoryField
        # Adjust fields as needed
        fields = ('CREATED', 'RESOURCE', 'ACTION', 'CHANGES')
