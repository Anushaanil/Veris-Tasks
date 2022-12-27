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

class EmployeeSerializer(serializers.ModelSerializer):
    #rname = serializers.CharField(source='role.role_name')
    #mgr_id = Employee.objects.values_list('manager_id', flat=True)

    class Meta:
        model = Employee
        fields = ['first_name','last_name','role','manager_id']

class EmployeeMgrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['emp_id']
