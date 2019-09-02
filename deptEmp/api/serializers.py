from rest_framework import serializers
from deptEmp.models import Department, Employee, User

class DepartmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Department
		fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
	user_id = serializers.IntegerField()
	department_id = serializers.IntegerField()

	class Meta:
		model = Employee
		fields = ['id', 'user_id', 'department_id' , 'full_name', 'email', 'title', 'cell_phone', 'work_phone', 'home_phone', 'man_of_month', 'address', 'profile']

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'password', 'is_admin']
		extra_kwargs = {'password' : {'write_only':True, 'required':True }}
