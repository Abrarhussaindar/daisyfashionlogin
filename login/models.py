from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from typing import Iterable
from django.core.validators import MaxValueValidator
from datetime import timedelta

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, intime, department, duration_time, out_time, logout_counter, login_counter, empid, name, designation, phone_number, permission, password=None):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            login_counter=login_counter,
            logout_counter=logout_counter,
            name=name,
            intime=intime,
            out_time=out_time,
            duration_time=duration_time,
            phone_number=phone_number,
            designation=designation,
            department=department,
            empid=empid,
            permission=permission,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, login_counter, department, duration_time, logout_counter, intime, out_time, email, empid, name, designation, phone_number, permission, password=None):
        user = self.create_user(
            email=email,
            username=username,
            name=name,
            designation=designation,
            department=department,
            empid=empid,
            login_counter=login_counter,
            logout_counter=logout_counter,
            intime=intime,
            out_time=out_time,
            duration_time=duration_time,
            phone_number=phone_number,
            permission=permission,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class ListField(models.TextField):

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['token'] = self.token
        return name, path, args, kwargs

    def to_python(self, value):
        class SubList(list):
            def __init__(self, token, *args):
                self.token = token
                super().__init__(*args)

            def __str__(self):
                return self.token.join(self)

        if isinstance(value, list):
            return value
        if value is None:
            return SubList(self.token)
        return SubList(self.token, value.split(self.token))

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        if not value:
            return
        assert(isinstance(value, Iterable))
        return self.token.join(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

permissions = (
    ('given', 'given'),
    ('not given', 'not given'),
)
from django.core.validators import MaxValueValidator, MinValueValidator
class Employee(AbstractBaseUser):
    name = models.CharField(verbose_name='Name', max_length=200, null=True)
    username = models.CharField(verbose_name='Username', max_length=20, null=True, unique=True)
    empid = models.CharField(verbose_name='Employee ID', max_length=20, null=True)
    permission = models.CharField(verbose_name='Permission', max_length=50, null=True, choices=permissions)
    
    work_time = models.DurationField(
            verbose_name='Work Time',
            default=timedelta(hours=0),  # Set the default value to 0 hours
            validators=[
                MinValueValidator(timedelta(hours=0)),  # Set the minimum value to 0 hours
                MaxValueValidator(timedelta(hours=8))   # Set the maximum value to 8 hours
            ]
        )

    remaining_time = models.DurationField(
        verbose_name='Remaining Time',
        default=timedelta(hours=0),  # Set the default value to 0 hours
        validators=[
            MinValueValidator(timedelta(hours=0))  # Set the minimum value to 0 hours
        ]
    )
    designation = models.CharField(verbose_name='Designation', max_length=50, null=True)
    department = models.CharField(verbose_name='Department', max_length=50, null=True)
    phone_number = models.CharField(verbose_name='Phone Number', max_length=10, null=True)
    login_counter = models.IntegerField(verbose_name="No. Of LogIns", default=0, null=True)
    logout_counter = models.IntegerField(verbose_name="No. Of LogOuts", default=0, null=True)

    intime = models.CharField(verbose_name='Current Login Time', max_length=200, null=True)
    out_time = models.CharField(verbose_name='Previous LogOut Time', max_length=200, null=True)
    duration_time = models.CharField(verbose_name='Last Login Duration', max_length=200, null=True)

    login_list = ListField(verbose_name="Login List", null=True)
    logout_list = ListField(verbose_name="Logout List", null=True)
    duration_list = ListField(verbose_name="Login Duration List", null=True)

    daily_login_list = ListField(verbose_name="Daily Login List", null=True)
    weekly_login_list = ListField(verbose_name="Weekly Login List", null=True)
    monthly_login_list = ListField(verbose_name="Monthly Login List", null=True)

    daily_logout_list = ListField(verbose_name="Daily Logout List", null=True)
    weekly_logout_list = ListField(verbose_name="Weekly Logout List", null=True)
    monthly_logout_list = ListField(verbose_name="Monthly Logout List", null=True)

    daily_duration_list = ListField(verbose_name="Daily Duration List", null=True)
    weekly_duration_list = ListField(verbose_name="Weekly Duration List", null=True)
    monthly_duration_list = ListField(verbose_name="Monthly Duration List", null=True)

    login_time = models.DateTimeField(verbose_name='Login Time', null=True, blank=True)
    logout_time = models.DateTimeField(verbose_name='Logout Time', null=True, blank=True)
    duration = models.DurationField(verbose_name='Login Duration', null=True, blank=True)
    

    last_weekly_update = models.DateField(verbose_name="Last Weekly Update", null=True)
    last_monthly_update = models.DateField(verbose_name="Last Monthly Update", null=True)

    email = models.EmailField(verbose_name='Email', max_length=60, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_teamLead = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'phone_number', 'email', 'empid', 'designation', 'department', 'intime', 'logout_counter', 'login_counter', 'out_time', 'duration_time', 'permission']

    objects = MyUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    # @property
    # def remaining_time(self):
    #     total_work_time = self.work_time.total_seconds()
    #     max_work_time = 8 * 3600  # 8 hours in seconds
    #     remaining_seconds = max_work_time - total_work_time
    #     return timedelta(seconds=remaining_seconds)
    
    def calculate_duration(self):
        if self.login_time and self.logout_time:
            # Convert login_time and logout_time to the same timezone
            login_time = self.login_time.astimezone(timezone.utc)
            logout_time = self.logout_time.astimezone(timezone.utc)

            # Calculate the duration
            self.duration = logout_time - login_time
        else:
            self.duration = None

        # Calculate the work_time

        self.save()


# class ChangePermissions(models.Model):
#     emp = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL)
#     permission = models.CharField(verbose_name='Permission', max_length=50, null=True, choices=permissions)

#     def __str__(self):
#         return self.permission
from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=Employee)
def update_remaining_time(sender, instance, **kwargs):
    total_work_time = instance.work_time.total_seconds()
    max_work_time = 8 * 3600  # 8 hours in seconds
    remaining_seconds = max_work_time - total_work_time
    remaining_time = timedelta(seconds=remaining_seconds)

    if remaining_time < timedelta(seconds=0):
        instance.remaining_time = timedelta(seconds=0)
    else:
        instance.remaining_time = remaining_time