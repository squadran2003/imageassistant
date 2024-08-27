from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.conf import settings
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
    processed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name
