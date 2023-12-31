# Generated by Django 3.2.11 on 2023-07-19 11:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0042_alter_employee_permission'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangePermissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.CharField(choices=[('given', 'given'), ('not given', 'not given')], max_length=50, null=True, verbose_name='Permission')),
                ('emp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
