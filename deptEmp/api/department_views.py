from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core import serializers

from deptEmp.models import Department

from .serializers import DepartmentSerializer

# department views start from here

class DepartmentView(viewsets.ModelViewSet): #DeptView -> Department_view
	serializer_class = DepartmentSerializer

	def get_queryset(self):
		departments = []

		department_name = self.request.query_params.get('department_name', None)
		department_id = self.request.query_params.get('id', None)

		if department_name is not None:
			departments = Department.objects.filter(department_name__iexact = department_name)
			if departments and str(departments[0].id) == str(department_id):
				departments = []
		else:
			departments = Department.objects.all()
		return departments
