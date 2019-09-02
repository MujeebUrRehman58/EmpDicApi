from django.urls import path, include
from . import user_views
from . import employee_views
from . import department_views
from rest_framework import routers

from deptEmp.models import Employee, Department, User

router = routers.DefaultRouter()
router.register('departments', department_views.DepartmentView, basename='Department')
router.register('employees', employee_views.EmployeeView, basename='Employee')
router.register('users', user_views.UserView, basename='User')

urlpatterns = [
path('', include(router.urls)),
path('employees/<pk>/profile/', employee_views.image),
]