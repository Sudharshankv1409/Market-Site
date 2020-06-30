from django.contrib import admin
from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['email','phone_number','first_name','last_name','date_of_birth','gender']
    empty_value_display = 'EMPTY'
admin.site.register(User, UserAdmin)
