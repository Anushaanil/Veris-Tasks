from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.ModelSerializer):

    building_number = serializers.IntegerField(source='address.building_number')
    street_address = serializers.CharField(source='address.street_address')
    city = serializers.CharField(source='address.city')
    state = serializers.CharField(source='address.state')
    zipcode = serializers.IntegerField(source='address.zipcode')

    class Meta:
        model = Users
        fields = ('user_name','birth_date','address', 'building_number', 
                  'street_address', 'city', 'state', 'zipcode')