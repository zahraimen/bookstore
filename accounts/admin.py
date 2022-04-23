from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreation, CustomUserChange
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreation
    form = CustomUserChange
    model = CustomUser
    list_display = ['username','email','age','is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('age',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets +(
        (None, {'fields': ('age',)})
        ,)


admin.site.register(CustomUser, CustomUserAdmin)
