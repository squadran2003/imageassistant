# myapp/storage_backends.py
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class StaticStorage(S3Boto3Storage):
    location = 'static'
    custom_domain = settings.CLOUDFRONT_DOMAIN


class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = True
    custom_domain = settings.CLOUDFRONT_DOMAIN
