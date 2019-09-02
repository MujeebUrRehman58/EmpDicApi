from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee, Department, User

class Admin(UserAdmin):
    list_display = ('username', 'is_admin', 'is_staff', 'date_joined', 'last_login',)
    search_fields = ('username',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

# Register your models here.
admin.site.register(User, Admin)
admin.site.register(Employee)
admin.site.register(Department)