from django.contrib import admin
from .models import User, Position, Department

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['image_tag','user_fname','user_lname','user_email','user_department','user_position']

class PositionAdmin(admin.ModelAdmin):
    list_display = ['position_id','position_name']

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['department_id','department_name']
    



admin.site.register(User,UserAdmin)
admin.site.register(Position,PositionAdmin)
admin.site.register(Department,DepartmentAdmin)
