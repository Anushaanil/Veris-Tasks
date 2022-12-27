from django.urls import path
from .views import EmployeeParentDetails, EmployeeChildrenDetails

urlpatterns = [
    path('display/parent/', EmployeeParentDetails.as_view()),
    path('display/children/', EmployeeChildrenDetails.as_view()),
]