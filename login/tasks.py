# # tasks.py

# from celery import shared_task
# from .models import Employee

# @shared_task
# def update_weekly_duration():
#     employees = Employee.objects.all()

#     for emp in employees:
#         if emp.daily_duration_list:
#             # Add daily durations to weekly_duration_list
#             for duration_str in emp.daily_duration_list:
#                 emp.weekly_duration_list.append(parse_duration_time(duration_str).total_seconds())
#             emp.save()

#             # Reset daily_duration_list and duration_list
#             emp.daily_duration_list = []
#             emp.duration_list = []
#             emp.save()
