from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
import os


@receiver(post_delete, sender='images.Image')
def delete_old_image(sender, instance, **kwargs):
    print('deleting old image')
    print(instance.image.path)
    # to fix , images not getting deleted
    if not settings.DEBUG:
        if os.path.isfile(instance.image.url):
            os.remove(instance.image.url)
    else:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


class Image(models.Model):
    image = models.ImageField()
    processed = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name
