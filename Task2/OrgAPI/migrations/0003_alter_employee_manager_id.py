# Generated by Django 4.1.4 on 2022-12-26 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrgAPI', '0002_role_alter_employee_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='manager_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]