from celery import shared_task
from images.models import Image
from PIL import Image as PILImage
from PIL import ImageOps
from urllib.request import urlopen
from io import BytesIO
from django.core.files.base import ContentFile
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from django.conf import settings
import os




@shared_task
def create_greyscale(image_id):
    s3 = boto3.client(
        's3'
    )
    file = Image.objects.get(pk=image_id)
    if not settings.DEBUG:
        img = PILImage.open(urlopen(file.image.url))
    else:
        img = PILImage.open(file.image.path)
    grayscale_img = img.convert("L")
    # Save the grayscale image to a BytesIO object
    img_io = BytesIO()
    grayscale_img.save(img_io, format='png')
    img_content = ContentFile(img_io.getvalue())
    # dont want a new folder , just want to override the uploaded image
    if not settings.DEBUG:
        # in prod saving the image to s3 and later updating the image field via lambda
        s3.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=f"media/{image_id}_{file.image.name}",
            Body=img_io.getvalue()
        )
    else:
        file.image.save(file.image.name, img_content)
        file.processed = True
        file.save()


@shared_task
def remove_background(image_id):
    file = Image.objects.get(pk=image_id)
    img_io = BytesIO()
    file_name_for_s3 = f"3*{image_id}_{file.image.name}"
    # filename should be service_id*image_id
    if not settings.DEBUG:
        img = PILImage.open(urlopen(file.image.url))
        img.save(img_io, format='png')
    else:
        from rembg import remove, new_session
        s3 = boto3.client('s3')
        img = PILImage.open(file.image.path)
        image_bg_removed = remove(
            img
        )
        image_bg_removed.save(img_io, format='png')
        img_content = ContentFile(img_io.getvalue())
    if not settings.DEBUG:
        # in prod saving the image to s3 and later updating the image field via lambda
        s3.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=f"media/{file_name_for_s3}",
            Body=img_io.getvalue()
        )
    else:
        file.image.save(file.image.name, img_content)
        file.processed = True
        file.save()


@shared_task
def resize_image(image_id, width, height):
    print("resizing")
    print(image_id, width, height)
    s3 = boto3.client('s3')
    # from rembg import remove
    size = (width, height)
    file = Image.objects.get(pk=image_id)
    if not settings.DEBUG:
        img = PILImage.open(urlopen(file.image.url))
    else:
        img = PILImage.open(file.image.path)
    print(file.image.name)
    img_io = BytesIO()
    img_resized = img.resize(size)
    img_resized.save(img_io, format='png', quality=100)
    img_content = ContentFile(img_io.getvalue())
    if not settings.DEBUG:
        # in prod saving the image to s3 and later updating the image field via lambda
        s3.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=f"media/{image_id}_{file.image.name}",
            Body=img_io.getvalue()
        )
    else:
        file.image.save(file.image.name, img_content)
        file.processed = True
        file.save()


@shared_task
def create_thumbnail(image_id):
    s3 = boto3.client('s3')
    file = Image.objects.get(pk=image_id)
    if not settings.DEBUG:
        img = PILImage.open(urlopen(file.image.url))
    else:
        img = PILImage.open(file.image.path)
    img_io = BytesIO()
    img.thumbnail((1280, 720))
    img.save(img_io, format='png', quality=100)
    img_content = ContentFile(img_io.getvalue())
    if not settings.DEBUG:
        # in prod saving the image to s3 and later updating the image field via lambda
        s3.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=f"media/{image_id}_{file.image.name}",
            Body=img_io.getvalue()
        )
    else:
        # in dev using celery to process the image
        file.image.save(file.image.name, img_content)
        file.processed = True
        file.save()

