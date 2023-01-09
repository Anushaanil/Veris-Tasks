from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .serializer import EmployeeMgrSerializer, RoleSerializer, DepartmentSerializer
from .models import Employee, Role, Department
from rest_framework import generics
from rest_framework.views import APIView
import json


def add_children(node, data):
    for item in data:
        if item['manager_id'] == node[list(node.keys())[0]]['emp_id']:
            item_role = Role.objects.get(role_id = item['role']).role_name
            item_name = item['first_name']+ ' ' + item['last_name']

            child = {item['emp_id']:{'emp_id':item['emp_id'], 'name': item_name, 'role': item_role, 'children':[]}}

            node[list(node.keys())[0]]['children'].append(child)
            add_children(child, data)

def find_val(d, k):
    if str(k) in d: return d[str(k)]
    for v in d.values():
        if isinstance(v, dict):
            a = find_val(v, k)
            if a is not None: return a

        elif isinstance(v,list):
            for i in v:
                if isinstance(i, dict):
                    a = find_val(i, k)
                    if a is not None: return a
    return None

class EmployeeHierarchy(APIView):
    ''' Display the entire Organization Structure'''

    def get(self, *args, **kwargs):

        emps = Employee.objects.values('emp_id','first_name','last_name','role','manager_id').order_by('-role')
    
        data = [val for val in emps]
        
        root_node = emps.get(manager_id = None)

        root_role = Role.objects.get(role_id = root_node['role']).role_name
        root_name = root_node['first_name'] + ' ' + root_node['last_name']

        root = {root_node['emp_id']:
        {'emp_id':root_node['emp_id'], 'name': root_name, 'role': root_role, 'children':[]}}
       
        add_children(root, data)

        return JsonResponse(root, safe=False, json_dumps_params={'indent':2})

def generate_hierarchy():
    res = EmployeeHierarchy().get().content
    json_data = json.loads(res)
    return json_data

class EmployeeParentDetails(generics.GenericAPIView):
    ''' Fetch Parent Details of an Employee using Employee ID'''

    serializer_class = EmployeeMgrSerializer

    def post(self,request):
        emp_id = request.data.get('emp_id')

        try:
            emp = Employee.objects.get(emp_id = emp_id)

            if emp:
                if emp.manager_id:
                    parent_detail = Employee.objects.get(emp_id = emp.manager_id)
                    parent_details = {'Employee Id' : parent_detail.emp_id,
                                    'Name' : parent_detail.first_name + ' ' + parent_detail.last_name,
                                    'Role' : parent_detail.role.role_name,
                                    'Department' : parent_detail.department.dept_name}
                else:
                    parent_details = {"error" : "This employee node is a top node!"}
        except:
            parent_details = {"error" : "invalid employee Id"}

        return render(request, 'parent_details.html', {'parent_details': parent_details})

class EmployeeChildrenDetails(generics.GenericAPIView):
    ''' Fetch Children Details of an Employee using Employee ID'''

    serializer_class = EmployeeMgrSerializer

    def post(self,request):
        emp_id = request.data.get('emp_id')
        try:
            emp = Employee.objects.get(emp_id = emp_id)
            if emp:
                data = []
                json_data = generate_hierarchy()
                hierarchy = find_val(json_data, emp_id)

                if hierarchy:
                    children = hierarchy['children']
                    if children:
                        keys = [int(key) for child in children for key in child.keys()]
                        for key in keys:
                            child_detail = Employee.objects.get(emp_id = key)
                            child_details = {'Employee Id' : child_detail.emp_id,
                                            'Name' : child_detail.first_name + ' ' + child_detail.last_name,
                                            'Role' : child_detail.role.role_name,
                                            'Department' : child_detail.department.dept_name}
                            data.append(child_details)
                    else:
                        data = [{"error" : "This employee node is a leaf node!"}]
        except:
            data = [{"error" : "invalid employee Id"}]
        
        return render(request, 'children_details.html', {'children_details': data})

class DisplayRoles(generics.ListAPIView):
    ''' Display all the Roles of an Organization '''

    serializer_class = RoleSerializer
    queryset = Role.objects.all().order_by('role_rank')

class DisplayDepartments(generics.ListAPIView):
    ''' Display all the Departments of an Organization '''

    serializer_class = DepartmentSerializer
    queryset = Department.objects.all().order_by('dept_id')

class CheckEmployeeExists(generics.GenericAPIView):
    ''' Check if an Employee exists under the specified Manager Hierarchy '''
    
    serializer_class = EmployeeMgrSerializer
    
    def post(self,request):
        emp_id = request.data.get('emp_id')
        mgr_id = request.data.get('manager_id')

        data = list(Employee.objects.filter(emp_id= emp_id))
        json_data = generate_hierarchy()

        if data:
            try:
                hierarchy = find_val(json_data, mgr_id)

                if(find_val(hierarchy, emp_id)):
                    return HttpResponse(True)
                else:
                    return HttpResponse(False)
            except:
                return HttpResponse('Invalid Manager Id!')
        else:
            return HttpResponse('Invalid Employee Id!')

