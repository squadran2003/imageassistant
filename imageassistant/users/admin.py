from django.contrib import admin
from users.models import CustomUser, Credit, FeatureFlag, BaredUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Credit)
admin.site.register(FeatureFlag)

class BaredUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'reason', 'created_at')
    search_fields = ('user__email', 'first_name', 'last_name', 'reason')
    list_filter = ('created_at',)

admin.site.register(BaredUser, BaredUserAdmin)
