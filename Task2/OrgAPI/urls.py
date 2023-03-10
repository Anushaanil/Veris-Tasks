from django.urls import path
from .views import (
    EmployeeParentDetails, 
    EmployeeChildrenDetails, 
    EmployeeHierarchy,
    DisplayRoles,
    DisplayDepartments,
    CheckEmployeeExists
)

urlpatterns = [
    path('display/parent/', EmployeeParentDetails.as_view()),
    path('display/children/', EmployeeChildrenDetails.as_view()),
    path('display/hierarchy/', EmployeeHierarchy.as_view()),
    path('display/roles/', DisplayRoles.as_view()),
    path('display/departments/', DisplayDepartments.as_view()),
    path('display/check/', CheckEmployeeExists.as_view()),
]