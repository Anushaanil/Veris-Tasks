from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer,RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics

from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_list_or_404


@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    ''' Creates token after saving a new user '''
    if created:
        Token.objects.create(user=instance)

class UserListFilter(generics.ListAPIView):
    ''' Lists all users, filter active users, filter staff users and search users based on name'''
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        path = self.request.get_full_path().split('/')
        users = get_user_model().objects.all()

        if path[2] == 'all':
            return users

        elif path[2] == 'active':
            return users.filter(is_active=True)

        elif path[2] == 'staff':
            return users.filter(is_staff=True)
        
        else:
            usernames = users.filter(username__contains= path[2])
            return get_list_or_404(usernames)

class UserSignupAPI(generics.CreateAPIView):
    ''' Register a new user '''
    http_method_names = ["post"]
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
class UserLoginAPI(generics.CreateAPIView):
    ''' Login user using email and password '''
    http_method_names = ["post"]
    authentication_classes = (TokenAuthentication,)
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self,request,*args,**kwargs):
        email = request.data['email']
        user = get_user_model().objects.get(email= email)
        if user.check_password(request.data['password']):
            serializer = UserSerializer(user)
            data = serializer.data
            token, _ = Token.objects.get_or_create(user=user)
            data["message"] = serializer.data["email"] + " logged in successfully!"
            data["token"] = str(token)
            return Response(data)
        else:
            return Response('Enter valid credentials!')
        
class UserLogoutAPI(APIView):
    ''' Logout an existing user with token '''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    
    def post(self,request,*args,**kwargs):
        request.user.auth_token.delete()
        return Response('User Logged out successfully')