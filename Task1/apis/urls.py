from django.urls import path
from .views import UserSignupAPI, UserLoginAPI, UserLogoutAPI, UserListFilter
from rest_framework.authtoken import views as drf_views

urlpatterns = [
    path('filter/all', UserListFilter.as_view()),
    path('filter/active', UserListFilter.as_view()),
    path('filter/staff', UserListFilter.as_view()),
    path('filter/<str:name>', UserListFilter.as_view()),
    path('signup/', UserSignupAPI.as_view()),
    path('login/', UserLoginAPI.as_view()),
    path('logout/', UserLogoutAPI.as_view()),
    path('api-token-auth/', drf_views.obtain_auth_token),
]

