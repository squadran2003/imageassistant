from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.conf import settings
from django.db.models import JSONField
import os
import boto3


@receiver(post_delete, sender='images.Image')
def delete_old_image(sender, instance, **kwargs):
    print('deleting old image')
    # to fix , images not getting deleted
    if not settings.DEBUG:
        boto3.client('s3').delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=f"media/{instance.id}_{instance.image.name}"
        )
    else:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


class Image(models.Model):
    image = models.ImageField(max_length=500)
    alternate_url = models.TextField(blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    prompt = models.TextField(blank=True, null=True)
    processed = models.BooleanField(default=False)
    aspect_ratio = models.CharField(max_length=50, default="16:9")
    ai_response = JSONField(blank=True, null=True)
    payment_made = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name
    



services = (
    ('Greyscale', 'Greyscale'),
    ('Remove Background', 'Remove Background'),
    ('Resize', 'Resize'),
    ('Thumbnail', 'Thumbnail'),
    ('Enhancement', 'Enhancement'),
    ('Cropping', 'Cropping'),
    ('GenerateImage', 'GenerateImage'),
)


class Service(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=255, choices=services)
    description = models.TextField(blank=True, null=True)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)
    free = models.BooleanField(default=True)
    cost = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
