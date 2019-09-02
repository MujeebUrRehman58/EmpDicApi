from rest_framework import viewsets
from deptEmp.models import User
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core import serializers

from .serializers import UserSerializer

# User views starts from here

class UserView(viewsets.ModelViewSet):	# UserView to User_view
	serializer_class = UserSerializer

	def get_queryset(self):
		users = []
		
		username = self.request.query_params.get('username', None)
		user_id = self.request.query_params.get('id', None)

		if username is not None:
			users = User.objects.filter(username__iexact=username)
			if users and str(users[0].id) == str(user_id):
				users = []
		else:
			users = User.objects.all()
		return users