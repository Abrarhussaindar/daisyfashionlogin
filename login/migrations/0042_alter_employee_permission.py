# Generated by Django 3.2.11 on 2023-07-19 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0041_employee_remaining_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='permission',
            field=models.CharField(choices=[('given', 'given'), ('not given', 'not given')], max_length=50, null=True, verbose_name='Permission'),
        ),
    ]
