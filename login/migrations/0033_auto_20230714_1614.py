# Generated by Django 3.2.11 on 2023-07-14 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0032_auto_20230714_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='duration',
            field=models.DurationField(blank=True, null=True, verbose_name='Login Duration'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='login_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Login Time'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='logout_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Logout Time'),
        ),
    ]
