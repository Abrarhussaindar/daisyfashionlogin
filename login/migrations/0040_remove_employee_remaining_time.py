# Generated by Django 3.2.11 on 2023-07-19 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0039_employee_remaining_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='remaining_time',
        ),
    ]
