from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.http import JsonResponse
from datetime import datetime, timedelta
import pytz
from django.db.models import Sum
from dateutil import parser
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
import time
from .models import Employee
from datetime import time
from django.http import JsonResponse
from django.http import JsonResponse
from datetime import datetime, timedelta
from dateutil import parser
import pytz

# Define constants for work time and remaining time limits
MAX_WORK_TIME = timedelta(hours=8)
MIN_REMAINING_TIME = timedelta(hours=0)


@login_required(login_url='login')
def get_remaining_time(request):
    emp = request.user
    remaining_time = emp.remaining_time
    formatted_remaining_time = str(remaining_time)
    return JsonResponse({'remaining_time': formatted_remaining_time})

@require_GET
def update_work_time(request):
    emp = request.user

    while True:
        # Calculate the updated work time
        total_time = timedelta()
        for duration_str in emp.daily_duration_list:
            total_time += parse_duration_time(duration_str)

        # Format the work time in h:m:s format
        work_time_str = str(total_time)

        # Save the work time to the employee instance
        emp.work_time = total_time
        emp.save()

        # Wait for 10 seconds before calculating again
        time.sleep(10)



@login_required(login_url='login')
@require_GET
def get_work_time(request):
    emp = request.user
    work_time = emp.work_time
    remaining_time = emp.remaining_time
    login_time_str = request.session.get('login_time')
    current_time = datetime.now(pytz.timezone('Asia/Kolkata'))
    
    if login_time_str:
        login_time = parser.isoparse(login_time_str).astimezone(pytz.timezone('Asia/Kolkata'))
        duration = current_time - login_time
        today = current_time.date()
        total_work = work_time + duration

        total_work_time = timedelta(hours=8)
        remaining_time = total_work_time - total_work

        formatted_work_time = format_timedelta(total_work)
        formatted_remaining_time = format_timedelta(remaining_time)

        return JsonResponse({'work_time': formatted_work_time, 'remaining_time': formatted_remaining_time})
    
    # If there is no login_time_str, return 0 duration
    formatted_work_time = format_timedelta(work_time)
    formatted_remaining_time = format_timedelta(remaining_time)

    return JsonResponse({'work_time': formatted_work_time, 'remaining_time': formatted_remaining_time})

def format_timedelta(td):
    seconds = int(td.total_seconds())
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def user_login(request):
    department_categories = ["Management/Admin", "Content Writer", "HR", "SEO", "Sales", "Design & Development"]
    permission = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('Password')
        department = request.POST.get('department')

        employee = authenticate(request, department=department, username=username, password=password)

        if employee is not None and employee.permission == "given":  # Check permission
            employee.login_counter += 1
            login(request, employee)

            # Reset the counter to 0 on login
            request.session['counter_time'] = 0

            current_time = datetime.now(pytz.timezone('Asia/Kolkata'))
            current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

            employee.login_list.append(current_time_str)
            employee.intime = current_time_str
            employee.login_time = current_time
            previous_login_time_str = request.session.get('login_time')

            employee.daily_login_list.append(current_time_str)
            employee.save()

            login_time = parser.isoparse(previous_login_time_str).astimezone(pytz.timezone('Asia/Kolkata')) if previous_login_time_str else current_time
            request.session['login_time'] = current_time.isoformat()

            if previous_login_time_str:
                previous_duration = current_time - login_time
                counter_time = request.session.get('counter_time', 0) + previous_duration.total_seconds()
                request.session['counter_time'] = counter_time

            employee.login_time = current_time
            employee.save()

            return redirect('home')
        else:
            permission = "not given"

    context = {
        "department_categories": department_categories,
        "permission": permission
    }
    return render(request, "login.html", context)


@login_required
def user_logout(request):
    emp = request.user

    current_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
    emp.logout_list.append(current_time)
    emp.daily_logout_list.append(current_time)

    t1 = datetime.strptime(emp.intime, "%Y-%m-%d %H:%M:%S")
    t2 = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
    duration_time = t2 - t1

    emp.duration_list.append(str(duration_time))
    emp.daily_duration_list.append(str(duration_time))
    emp.logout_counter += 1
    emp.logout_time = datetime.now()
    emp.out_time = current_time
    emp.duration = duration_time
    emp.duration_time = str(t2 - t1)  # Update the duration_time calculation
    emp.permission = "not given"
    total_time = timedelta()
    for duration_str in emp.daily_duration_list:
        print("d_str: ",duration_str)
        total_time += parse_duration_time(duration_str)

    # Format the work time in h:m:s format
    work_time_str = str(total_time)

    # Save the work time to the employee instance
    emp.work_time = total_time
    total_work_time = timedelta(hours=8)
    remaining_time = total_work_time - emp.work_time
    # Update emp.remaining_time
    emp.remaining_time = remaining_time
        # emp.save()

    # Save the changes to the employee
    emp.save()
    print("emp permission after logout: ", emp.permission)
    print("after save emp_du: ", emp.duration)
    request.session['counter_time'] = 0
    request.session['login_time'] = None

    logout(request)
    return redirect('login')


def create_new_user(request):
    form = CreateEmployee()
    if request.method == 'POST':
        form = CreateEmployee(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}
    return render(request, "register.html", context)

@login_required(login_url='login')  
def change_permission(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        permission = request.POST.get('permission')
        try:
            employee = Employee.objects.get(pk=employee_id)
            employee.permission = permission
            employee.save()
            return redirect('home') 
        except Employee.DoesNotExist:
            pass

    employees = Employee.objects.all()
    context = {
        'employees': employees
    }
    return render(request, "change_permission.html", context)


@login_required(login_url='login')
def home(request):
    emp = request.user
    duration = None
    login_time_str = request.session.get('login_time')
    current_time = datetime.now(pytz.timezone('Asia/Kolkata'))
    employees = Employee.objects.filter(department=emp.department)

    if login_time_str:
        login_time = parser.isoparse(login_time_str).astimezone(pytz.timezone('Asia/Kolkata'))
        duration = current_time - login_time
        today = current_time.date()
        total_work = emp.work_time + duration
        total_work_seconds = total_work.total_seconds()
        total_work_time = timedelta(hours=8)
        remaining_time = total_work_time - total_work
        total_work_str = str(total_work)
        total_work_formatted = total_work_str.rjust(8, '0')

        if emp.last_weekly_update and emp.last_weekly_update.isocalendar()[1] < today.isocalendar()[1]:
            # Update weekly lists
            weekly_login_count = emp.daily_login_list.filter(login_time__week=emp.last_weekly_update.isocalendar()[1]).count()
            emp.weekly_login_list.append(weekly_login_count)
            emp.weekly_logout_list.append(emp.daily_logout_list.filter(logout_time__week=emp.last_weekly_update.isocalendar()[1]).count())
            weekly_duration = emp.daily_duration_list.filter(duration__week=emp.last_weekly_update.isocalendar()[1]).aggregate(total_duration=Sum('duration'))['total_duration']
            emp.weekly_duration_list.append(weekly_duration.total_seconds() if weekly_duration else 0)

        if emp.last_monthly_update and emp.last_monthly_update.month < today.month:
            # Update monthly lists
            monthly_login_count = emp.daily_login_list.filter(login_time__month=emp.last_monthly_update.month).count()
            emp.monthly_login_list.append(monthly_login_count)
            emp.monthly_logout_list.append(emp.daily_logout_list.filter(logout_time__month=emp.last_monthly_update.month).count())
            emp.monthly_duration_list.append(emp.daily_duration_list.filter(duration__month=emp.last_monthly_update.month).aggregate(total_duration=Sum('duration'))['total_duration'])

        emp.last_weekly_update = today
        emp.last_monthly_update = today

    context = {
        'emp': emp,
        'remaining_time': remaining_time,
        'employees': employees,
        'total_work_seconds': total_work_seconds,
        'total_work': total_work_formatted,
        'duration': duration.total_seconds() if duration else 0,
    }

    # if request.is_ajax():
    #     return JsonResponse({'total_work': total_work_formatted})

    return render(request, "home.html", context)


def admin(request):
    return render(request)


def parse_duration_time(duration_time_str):
    if duration_time_str:
        duration_parts = duration_time_str.split(':')
        if len(duration_parts) >= 3:  # Check if duration_parts has at least 3 elements
            hours = int(float(duration_parts[0]))
            minutes = int(float(duration_parts[1]))
            seconds = int(float(duration_parts[2]))
            return timedelta(hours=hours, minutes=minutes, seconds=seconds)
    return timedelta(seconds=0)