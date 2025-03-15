from django.contrib import admin
from users.models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')


admin.site.register(CustomUser, CustomUserAdmin)