from django.db import models

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin 
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
import boto3



class CustomManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.is_superuser = False
        user.is_staff = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    required_fields = ["email"]

    objects = CustomManager()

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    @property
    def is_admin(self):
        return self.is_superuser


class Credit(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.total}"


class FeatureFlag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    enabled = models.BooleanField(default=False)
    users = models.ManyToManyField(CustomUser, blank=True, help_text="Users for whom this flag is enabled. Leave empty for global.")

    def is_active_for(self, user=None):
        if self.enabled:
            return True
        if user and self.users.filter(pk=user.pk).exists():
            return True
        return False

    def __str__(self):
        return self.name

class BaredUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='bare_user')
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    reason = models.TextField(blank=True, null=True, help_text="Reason for being banned")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.first_name} {self.last_name}"

@receiver(post_delete, sender=CustomUser)
def delete_user(sender, instance, **kwargs):
    if not settings.DEBUG:
        s3 = boto3.client(
            's3'
        )
        images = instance.image_set.all()
        for image in images:
            # delete the image from s3
            try:
                s3.delete_object(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    Key=f"media/celery/{image.image.name}"
                )
            except Exception as e:
                print(f"Error deleting image {image.image.name}: {e}")
