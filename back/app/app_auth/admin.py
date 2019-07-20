from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInLine(admin.TabularInline):
    model = Profile
    can_delete = True
    verbose_name_plural = 'Profile'
    list_display = ('photo')


class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','email','is_staff','password',)
    inlines = (ProfileInLine,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)