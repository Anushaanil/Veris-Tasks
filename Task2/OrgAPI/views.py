from django.shortcuts import render
from .serializer import EmployeeMgrSerializer, EmployeeSerializer, RoleSerializer
from .models import Employee, Role, Department
from rest_framework import generics

def get_json_data():
    employees = {}

    parent_id = Employee.objects.values_list('manager_id', flat=True)
    emps= Employee.objects.filter(emp_id__in = parent_id)

    key = list(val['manager_id'] for val in emps.values('manager_id'))

    key = list(set(key))
    
    for i in range(len(key)):
        emp_val = Employee.objects.filter(manager_id = key[i])
        
        val = list(emp_val.values('emp_id','first_name', 'last_name','role','department'))

        if key[i] in employees:
            employees[key[i]] += val
        else:
            employees[key[i]] = val
        
    for k, v in employees.items():
        for k in range(len(v)):
            role = Role.objects.get(role_id = v[k]['role'])
            department = Department.objects.get(dept_id = v[k]['department'])
            v[k]['role'] = str(role)
            v[k]['department'] = str(department)
            
    return employees

class EmployeeParentDetails(generics.GenericAPIView):
    serializer_class = EmployeeMgrSerializer

    def post(self,request):
        emp_id = request.data.get('emp_id')

        try:
            emp = Employee.objects.get(emp_id = emp_id)
            parent_detail = Employee.objects.get(emp_id = emp.manager_id)

            parent_details = {
                                'emp_id' : parent_detail.emp_id,
                                'name' : parent_detail.first_name + ' ' + parent_detail.last_name,
                                'role' : parent_detail.role.role_name
                            }
        except:
            parent_details = {
                "error" : "invalid employee Id"
            }
        return render(request, 'parent_details.html', {'parent_details':parent_details})

class EmployeeChildrenDetails(generics.GenericAPIView):
    serializer_class = EmployeeMgrSerializer

    def post(self,request):
        emp_id = request.data.get('emp_id')
        try:
                res = get_json_data()
                data = res[emp_id]
        except:
            data = [{"error" : "invalid employee Id"}]
        
        return render(request, 'children_details.html', {'children_details': data})

class EmployeeHierarchy(generics.ListAPIView):
    http_method_names = ["get"]
    serializer_class = EmployeeSerializer
    
    def get_queryset(self):
        d = {}
        roles = list(Role.objects.values('role_rank','role_id'))
      
        for k in roles:
            employees = Employee.objects.filter(role = k['role_id'])

            for emp in employees:
                emp_details = {
                        'emp_name' : emp.first_name+' '+emp.last_name,
                        'role_name' : emp.role.role_name,
                        'children' : {}
                }
                
            if k['role_rank'] in d:
                d[k['role_rank']] += [emp_details]
            else:
                d[k['role_rank']] = [emp_details]

        print(d)
       
        queryset = Employee.objects.all().order_by('-role')
        return queryset

class DisplayRoles(generics.ListAPIView):
    serializer_class = RoleSerializer
    queryset = Role.objects.all().order_by('role_rank')