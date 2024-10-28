# myapp/storage_backends.py
from storages.backends.s3boto3 import S3Boto3Storage
from django.contrib.staticfiles import storage


class StaticStorage(storage.StaticFilesStorage):
    location = 'static'
    file_overwrite = True


class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = True
