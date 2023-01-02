from rest_framework import serializers
from .models import Employee, Role, Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class EmployeeMgrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['emp_id']
