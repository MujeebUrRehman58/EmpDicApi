from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.decorators import api_view

from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError

from deptEmp.models import Department, Employee, User
from .serializers import DepartmentSerializer, EmployeeSerializer, UserSerializer

# Employee views starts from here

class EmployeeView(viewsets.ModelViewSet): # EmpView -> empoyee_view
	serializer_class = EmployeeSerializer
	
	def get_queryset(self):
		employees = []

		email = self.request.query_params.get('email', None)
		username = self.request.query_params.get('username', None)
		name = self.request.query_params.get('full_name', None)
		department = self.request.query_params.get('department_name', None)
		man_of_month = self.request.query_params.get('man_of_month', None)

		if department == 'All':
			department = ''

		if man_of_month == 'Yes':
			man_of_month = True
		elif man_of_month == 'No':
			man_of_month = False
		else:
			man_of_month = ''

		if email is not None:
			employees = Employee.objects.filter(email__icontains = email, full_name__icontains = name, department_id__department_name__icontains = department)
		elif man_of_month is True and username is None and name is None:
			employees = Employee.objects.filter(man_of_month__icontains = man_of_month)
		elif username is not None:
			employees = Employee.objects.filter(full_name__icontains = name, user_id__username__icontains = username, man_of_month__icontains = man_of_month)
		else:
			employees = Employee.objects.all()

		return employees

	def create(self, request): # perform_create -> create_employee
		
		department_id = request.data.get('department_id', None)
		username = request.data.get('username', None)
		password = request.data.get('password', None)
		full_name = request.data.get('full_name', None)
		email = request.data.get('email', None)
		is_admin = request.data.get('level', None)
		title = request.data.get('title', None)
		cell_phone = request.data.get('cell_phone', None)
		home_phone = request.data.get('home_phone', None)
		work_phone = request.data.get('work_phone', None)
		address = request.data.get('address', None)
		man_of_month = request.data.get('man_of_month', None)
		
		if is_admin.lower() == 'admin':
			is_admin = True
		else:
			is_admin = False
		
		try:
			user = User.objects.create_user(username, is_admin, password=password)
		except IntegrityError as e:
			return Response({'error': 'Username is invalid or already exists'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		except Exception as e:
			return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		employee = Employee()
		employee.user_id = user.id
		user.is_admin = is_admin
		employee.full_name = full_name
		employee.email = email
		employee.title = title
		employee.cell_phone = cell_phone
		employee.home_phone = home_phone
		employee.work_phone = work_phone
		employee.address = address
		employee.department_id = department_id

		if man_of_month and str(man_of_month).lower() == 'true':
			Employee.objects.update(man_of_month=False)
			employee.man_of_month = True
		else:
			employee.man_of_month = False

		try:
			employee.save()
		except IntegrityError as e:
			user.delete()
			return Response({'error': 'Department ID doesn\'t exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		except Exception as e:
			user.delete()
			return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		employee = EmployeeSerializer(employee)
		return Response(employee.data, status=status.HTTP_201_CREATED)

	def update(self, request, pk=None): # perform_create -> create_employee
		department_id = request.data.get('department_id', None)
		username = request.data.get('username', None)
		full_name = request.data.get('full_name', None)
		email = request.data.get('email', None)
		title = request.data.get('title', None)
		is_admin = request.data.get('level', None)
		cell_phone = request.data.get('cell_phone', None)
		home_phone = request.data.get('home_phone', None)
		work_phone = request.data.get('work_phone', None)
		address = request.data.get('address', None)
		man_of_month = request.data.get('man_of_month', None)
		
		if str(is_admin).lower() == 'true':
			is_admin = True
		else:
			is_admin = False

		employee = get_object_or_404(Employee, pk=pk)
		employee.user.username = username
		employee.user.is_admin = is_admin
		employee.full_name = full_name
		employee.email = email
		employee.title = title
		employee.cell_phone = cell_phone
		employee.home_phone = home_phone
		employee.work_phone = work_phone
		employee.address = address

		if man_of_month and str(man_of_month).lower() == 'true':
			Employee.objects.update(man_of_month=False)
			employee.man_of_month = True
		else:
			employee.man_of_month = False

		try:
			employee.user.save()
			employee.save()
		except IntegrityError as e:
			exception_details = str(e)
			if 'username' in exception_details:
				return Response({'error': 'Username invalid or already exists'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
			elif 'department_id' in exception_details:
				return Response({'error': 'Department ID doesn\'t exist'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		except Exception as e:
			return Response({'error': 'The employee\'s data could not be updated due to an internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		employee = EmployeeSerializer(employee)
		return Response(employee.data, status=status.HTTP_202_ACCEPTED)

@api_view(['PATCH'])
def image(request, pk=None):
	profile = request.FILES.get('profile', None)
	if profile is not None:
		employee = get_object_or_404(Employee, pk=pk)
		employee.profile = profile
		employee.save()
		employee = EmployeeSerializer(employee)
		return Response(employee.data, status=status.HTTP_202_ACCEPTED)
	else:
		return Response(status=status.HTTP_400_BAD_REQUEST)
