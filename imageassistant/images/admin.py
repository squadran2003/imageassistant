from django.contrib import admin
from .models import Image, Service


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'alternate_url', 'processed', 'created')
    list_filter = ('processed', 'created')
    search_fields = ('id', 'image', 'processed', 'created')
    ordering = ('-created',)

admin.site.register(Image, ImageAdmin)
admin.site.register(Service)
