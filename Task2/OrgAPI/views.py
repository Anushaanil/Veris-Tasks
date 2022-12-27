from django.shortcuts import render
from .serializer import EmployeeMgrSerializer
from .models import Employee, Role
from rest_framework import generics

def get_json_data():
    employees = {}

    parent_id = Employee.objects.values_list('manager_id', flat=True)
    emps= Employee.objects.filter(emp_id__in = parent_id)

    key = list(val['manager_id'] for val in emps.values('manager_id'))

    key = list(set(key))
    
    for i in range(len(key)):
        emp_val = Employee.objects.filter(manager_id = key[i])
        #ids = Employee.objects.get(emp_id = key[i])
        #emp_name = ids.first_name + ' ' + ids.last_name
        
        val = list(emp_val.values('emp_id','first_name', 'last_name','role','department'))

        if key[i] in employees:
            employees[key[i]] += val
        else:
            employees[key[i]] = val
        
    for k, v in employees.items():
        for k in range(len(v)):
            role = Role.objects.get(role_id = v[k]['role'])
            v[k]['role'] = str(role)
            
    return employees

class EmployeeParentDetails(generics.GenericAPIView):
    serializer_class = EmployeeMgrSerializer

    def post(self,request):
        emp_id = request.data.get('emp_id')
        emp = Employee.objects.get(emp_id = emp_id)
        parent_detail = Employee.objects.get(emp_id = emp.manager_id)

        parent_details = {
                            'emp_id' : parent_detail.emp_id,
                            'name' : parent_detail.first_name + ' ' + parent_detail.last_name,
                            'role' : parent_detail.role.role_name
                        }

        return render(request, 'parent_details.html', {'parent_details':parent_details})

class EmployeeChildrenDetails(generics.GenericAPIView):
    serializer_class = EmployeeMgrSerializer

    def post(self,request):
        emp_id = request.data.get('emp_id')
        res = get_json_data()
        if emp_id in res.keys():
            data = res[emp_id]
        else:
            data = 'not found'
        return render(request, 'children_details.html', {'children_details':data})