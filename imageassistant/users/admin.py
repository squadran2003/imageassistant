from django.contrib import admin
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from users.models import CustomUser, Credit, FeatureFlag, BaredUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    actions = ['remove_inactive_users']

    def remove_inactive_users(self, request, queryset):
        """Remove users who haven't logged in over 90 days"""
        cutoff_date = timezone.now() - timedelta(days=90)
        # Get all users instead of using the selected queryset
        all_users = CustomUser.objects.all()
        
        # Filter for users who haven't logged in over 90 days
        # Also exclude staff users for safety
        inactive_users = all_users.filter(
            last_login__lt=cutoff_date,
            is_staff=False
        ).exclude(last_login__isnull=True)  # Exclude users who never logged in
        count = inactive_users.count()
        
        if count > 0:
            inactive_users.delete()
            self.message_user(
                request,
                f"Successfully removed {count} users who haven't logged in over 90 days.",
                messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                "No users found who haven't logged in over 90 days.",
                messages.INFO
            )
    
    remove_inactive_users.short_description = "Remove users inactive for 90+ days"


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Credit)
admin.site.register(FeatureFlag)

class BaredUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'reason', 'created_at')
    search_fields = ('user__email', 'first_name', 'last_name', 'reason')
    list_filter = ('created_at',)

admin.site.register(BaredUser, BaredUserAdmin)
