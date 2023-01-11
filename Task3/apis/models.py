from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

class Address(models.Model):
    building_number = models.IntegerField()
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.IntegerField()

    def __str__(self):
        return self.street_address

class Users(models.Model):
    user_name = models.CharField(max_length=200)
    birth_date = models.DateField(null=True, blank=True)
    address = models.ForeignKey(to=Address, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user_name
