from django.db import models

# Create your models here.

class Department(models.Model):
    dept_id = models.AutoField(primary_key=True, unique=True)
    dept_name = models.CharField(max_length=120)
    dept_location = models.CharField(max_length=120)

    def __str__(self):
        return self.dept_name

class Role(models.Model):
    role_id = models.AutoField(primary_key=True, unique=True)
    role_name = models.CharField(max_length=120)

    def __str__(self):
        return self.role_name

class Employee(models.Model):
    emp_id = models.AutoField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email_id = models.EmailField(unique=True)
    role = models.ForeignKey(to=Role,on_delete=models.CASCADE)
    department = models.ForeignKey(to=Department,on_delete=models.CASCADE)
    manager_id = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email_id

