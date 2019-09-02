from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
	def create_user(self, username, is_admin, password=None):
		if username is None:
			 raise ValueError("Users must have a username")
		if is_admin is None:
			raise ValueError("Users must have a level")
		
		user = self.model(
			username = username,
			is_admin = is_admin,
		)
		user.set_password(password)
		user.save(using=self._db)
		return user
	
	def create_superuser(self, username, is_admin, password):
		user = self.create_user(
			username = username,
			password = password,
			is_admin = True
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser):
	username = models.CharField(max_length=30, unique=True)
	date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['is_admin']

	objects = UserManager()

	def __str__(self):
		return self.username
	
	def has_perm(self, perm, obj=None):
		return self.is_admin
	
	def has_module_perms(self, app_label):
		return True

class Department(models.Model):
	department_name = models.CharField(max_length=255, unique=True) # dept_name -> department_name

	def __str__(self):
		return self.department_name

class Employee(models.Model):
	full_name = models.CharField(max_length=200)
	email = models.EmailField(max_length=70, unique=True)
	title = models.CharField(max_length=255)
	cell_phone = models.CharField(max_length=17, unique=True)
	home_phone = models.CharField(max_length=17, unique=True)
	work_phone = models.CharField(max_length=17, unique=True)
	address	= models.CharField(max_length=1024)
	man_of_month = models.BooleanField(default=False)	# manOfMonrh -> man_of_month
	profile	= models.ImageField(upload_to="images/", blank=True)	

	user = models.OneToOneField(User, on_delete=models.CASCADE) # user -> user_id
	department = models.ForeignKey(Department, on_delete=models.CASCADE) # dept -> department_id

	def __str__(self):
		return self.full_name