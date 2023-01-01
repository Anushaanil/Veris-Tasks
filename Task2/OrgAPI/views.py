from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .serializer import EmployeeMgrSerializer, RoleSerializer
from .models import Employee, Role, Department
from rest_framework import generics
from rest_framework.views import APIView
import json
from django.db.models import Q

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

def add_children(node, data):
    for item in data:
        if item['manager_id'] == node['emp_id']:
            item_role = Role.objects.get(role_id = item['role']).role_name
            item_name = item['first_name']+ ' ' + item['last_name']

            child = {'emp_id':item['emp_id'], 'name': item_name, 'role': item_role, 'children':[]}

            node['children'].append(child)
            add_children(child, data)

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

class EmployeeHierarchy(APIView):

    def get(self, *args, **kwargs):

        emps = Employee.objects.values('emp_id','first_name','last_name','role','manager_id').order_by('-role')
    
        data = [val for val in emps]
        
        root_node = emps.get(manager_id = None)

        root_role = Role.objects.get(role_id = root_node['role']).role_name
        root_name = root_node['first_name'] + ' ' + root_node['last_name']

        root = {'emp_id':root_node['emp_id'],
                'name': root_name,
                'role': root_role,
                'children':[]
               }
       
        add_children(root, data)

        return JsonResponse(root, safe=False, json_dumps_params={'indent':2})
        
class DisplayRoles(generics.ListAPIView):
    serializer_class = RoleSerializer
    queryset = Role.objects.all().order_by('role_rank')

class CheckEmployeeExists(generics.GenericAPIView):
    serializer_class = EmployeeMgrSerializer
    emp_obj  = EmployeeHierarchy()
    data = emp_obj.get().content
    json_data = json.loads(data)
    
    #print(json_data)

    def post(self,request):
        emp_id = request.data.get('emp_id')
        mgr_id = request.data.get('manager_id')

        data = list(Employee.objects.filter(emp_id= emp_id))
        return HttpResponse(data)

        '''
        try:
            emp = Employee.objects.get(emp_id = emp_id)
            mgr = Employee.objects.get(emp_id = mgr_id)

            if emp and mgr:
            
            if Employee.objects.filter(Q(emp_id= emp_id), Q(emp_id=mgr_id)).exists():
            
            data = Employee.objects.filter(emp_id= emp_id)
            return JsonResponse({"data" : data}, safe=False)
            else:
                return JsonResponse({"error" : "Employee doesn't exists!"}, safe=False)
        except:
            return JsonResponse({"error" : "invalid employee or manager Id"}, safe=False)

        '''
