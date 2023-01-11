from rest_framework import generics
from .models import Users
from .serializer import UsersSerializer

class UsersListView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer