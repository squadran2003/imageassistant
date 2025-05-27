from django.contrib import admin
from users.models import CustomUser, Credit, FeatureFlag

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Credit)
admin.site.register(FeatureFlag)