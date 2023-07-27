from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="user_logout"),
    path('register/', views.create_new_user, name="register"),
    path('get_work_time/', views.get_work_time, name='get_work_time'),
    path('admin/', views.admin, name="admin"),
    path('permissions/', views.change_permission, name="permissions")
]