from celery import shared_task
from images.models import Image
from PIL import Image as PILImage
from urllib.request import urlopen
from io import BytesIO
from django.core.files.base import ContentFile
import boto3
from django.conf import settings
import os
from urllib.request import urlopen
import cv2
import numpy as np
import urllib
import requests



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
            Key=f"media/celery/{image_id}_{file.image.name}",
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
    file_name_for_s3 = f"2*{image_id}_{file.image.name}"
    # filename should be service_id*image_id
    if not settings.DEBUG:
        img = PILImage.open(urlopen(file.image.url))
        img.save(img_io, format='png')
        img_io.seek(0)  # Important!
    else:
        from rembg import remove
        img = PILImage.open(file.image.path)
        image_bg_removed = remove(
            img
        )
        image_bg_removed.save(img_io, format='png')
        img_content = ContentFile(img_io.getvalue())
    if not settings.DEBUG:
        s3 = boto3.client('s3')
        # in prod saving the image to s3 and later updating the image field via lambda
        s3.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=f"media/celery/{file_name_for_s3}",
            Body=img_io.getvalue(),  # Uploading the image bytes
            ContentType='image/png'  # Set content type
        )
    else:
        file.image.save(file_name_for_s3, img_content)
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
            Key=f"media/celery/{image_id}_{file.image.name}",
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
            Key=f"media/celery/{image_id}_{file.image.name}",
            Body=img_io.getvalue()
        )
    else:
        # in dev using celery to process the image
        file.image.save(file.image.name, img_content)
        file.processed = True
        file.save()


@shared_task
def crop_image(image_id, x, y, width, height):
    s3 = boto3.client('s3')
    file = Image.objects.get(pk=image_id)
    if not settings.DEBUG:
        img = PILImage.open(urlopen(file.image.url))
    else:
        img = PILImage.open(file.image.path)
    img_io = BytesIO()
    print(x, y, width, height)
    img_cropped = img.crop((max(x, 0), max(y, 0), min(width+x, file.image.width), min(height+y, file.image.height)))
    img_cropped.save(img_io, format='png', quality=100)
    img_content = ContentFile(img_io.getvalue())
    if not settings.DEBUG:
        # in prod saving the image to s3 and later updating the image field via lambda
        s3.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=f"media/celery/{image_id}_{file.image.name}",
            Body=img_io.getvalue()
        )
    else:
        # in dev using celery to process the image
        file.image.save(file.image.name, img_content)
        file.processed = True
        file.save()


@shared_task
def enhance_image(image_id):
    s3 = boto3.client('s3')
    # https://api.stability.ai/v2beta/stable-image/edit/remove-background...
    file = Image.objects.get(pk=image_id)
    if not settings.DEBUG:
        img = PILImage.open(urlopen(file.image.url))
    else:
        img = PILImage.open(file.image.path)
    img_io = BytesIO()
    img.save(img_io, format='png', quality=100)
    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/upscale/fast",
        files={"image": img_io.getvalue()},
        headers={
            "Authorization": f"Bearer {settings.STABILITY_AI_KEY}",
            "accept": "image/*"
        },
        data={
            "output_format": "png",
        },
    )
    img_io.write(response.content)
    img_io.seek(0)
    img_content = ContentFile(img_io.getvalue())
    if not settings.DEBUG:
        # in prod saving the image to s3 and later updating the image field via lambda
        s3.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=f"media/celery/{image_id}_{file.image.name}",
            Body=img_io.getvalue()
        )
    else:
        # in dev using celery to process the image
        file.image.save(file.image.name, img_content)
        file.processed = True
        file.save()








