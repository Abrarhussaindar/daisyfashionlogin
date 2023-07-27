# Generated by Django 4.2.1 on 2023-05-20 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_alter_employee_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='intime',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Login Time'),
        ),
        migrations.AddField(
            model_name='employee',
            name='out_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='LogOut Time'),
        ),
    ]
