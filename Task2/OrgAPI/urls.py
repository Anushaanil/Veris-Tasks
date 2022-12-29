from django.urls import path
from .views import (
    EmployeeParentDetails, 
    EmployeeChildrenDetails, 
    EmployeeHierarchy,
    DisplayRoles
)

urlpatterns = [
    path('display/parent/', EmployeeParentDetails.as_view()),
    path('display/children/', EmployeeChildrenDetails.as_view()),
    path('display/hierarchy/', EmployeeHierarchy.as_view()),
    path('display/rhierarchy/', DisplayRoles.as_view()),
]