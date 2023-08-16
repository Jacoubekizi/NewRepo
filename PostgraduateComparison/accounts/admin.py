from django.contrib.auth.admin import UserAdmin
from .froms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, Student, Employee
from application.models import *
from application.admin import *
# Register your models here.




class CustomUserAdmin(UserAdmin):

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    model = CustomUser

    list_display = ['username','id' ,'email', 'first_name', 'is_admin', 'last_name', 'is_staff', 'is_employee']
    fieldsets = (
    (None, 
         {'fields':('email', 'password',)}
     ),
    ('User Information',
        {'fields':('username', 'first_name', 'last_name', 'is_student', 'is_employee')}
    ),
    ('Permissions', 
        {'fields':('is_staff', 'is_superuser', 'is_active', 'groups','user_permissions')}
    ),
    ('Registration', 
        {'fields':('date_joined', 'last_login',)}
    )
    )
    add_fieldsets = (
        (None, {'classes':('wide',),
            'fields':(
                'email','username', 'password1', 'password2','is_employee', 'is_staff'
            )}
            ),
        
    
    )

    search_fields = ("email",)
    ordering = ("email",)
    list_filter = ('is_employee', 'is_student')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student)
admin.site.register(Employee)

