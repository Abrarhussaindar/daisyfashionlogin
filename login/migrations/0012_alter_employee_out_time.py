# Generated by Django 4.2.1 on 2023-05-20 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0011_alter_employee_intime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='out_time',
            field=models.TimeField(null=True, verbose_name='LogOut Time'),
        ),
    ]
