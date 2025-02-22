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
import urllib.parse
import requests
import datetime



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
    s3 = boto3.client('s3')
    file = Image.objects.get(pk=image_id)
    if not settings.DEBUG:
        img = PILImage.open(urlopen(file.image.url))
    else:
        img = PILImage.open(file.image.path)
    img_io = BytesIO()
    img.save(img_io, format='png', quality=100)
    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/edit/remove-background",
        files={"image": img_io.getvalue()},
        headers={
            "Authorization": f"Bearer {settings.STABILITY_AI_KEY}",
            "accept": "image/*"
        },
        data={
            "output_format": "png",
        },
    )
    if response.status_code == 200:
        img_io = BytesIO()
        img_io.seek(0)
        img_io.write(response.content)
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
    else:
        print(response.status_code)
        print(response.headers.get("finish-reason"))
    file.processed = True
    file.save()


@shared_task
def resize_image(image_id, width, height):
    s3 = boto3.client('s3')
    # from rembg import remove
    size = (width, height)
    file = Image.objects.get(pk=image_id)
    if not settings.DEBUG:
        img = PILImage.open(urlopen(file.image.url))
    else:
        img = PILImage.open(file.image.path)
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
def enhance_image(image_id, prompt=None):
    s3 = boto3.client('s3')
    if not prompt:
        print("Prompt is required")
        return
    # https://api.stability.ai/v2beta/stable-image/edit/remove-background...
    file = Image.objects.get(pk=image_id)
    if not settings.DEBUG:
        img = PILImage.open(urlopen(file.image.url))
    else:
        img = PILImage.open(file.image.path)
    img_io = BytesIO()
    img.save(img_io, format='png', quality=100)
    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/upscale/conservative",
        files={"image": img_io.getvalue()},
        headers={
            "Authorization": f"Bearer {settings.STABILITY_AI_KEY}",
            "accept": "image/*"
        },
        data={
            "output_format": "png",
            "prompt": prompt
        },
    )
    # reset img_io
    img_io = BytesIO()
    if response.status_code == 200:
        img_io.seek(0)
        img_io.write(response.content)
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
    else:
        print(response.status_code)
        print(response.headers.get("finish-reason"))
    file.processed = True
    file.save()


@shared_task
def create_image_from_prompt(image_id, prompt):
    file = Image.objects.get(pk=image_id)
    file_name = f"{image_id}_prompt.png"
    # URL-encode the filename to replace spaces with %20
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={
            "authorization": f"Bearer {settings.STABILITY_AI_KEY}",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": prompt,
            "output_format": "png",
            "aspect_ratio": file.aspect_ratio
        },
    )
    img_io = BytesIO()
    if response.status_code == 200:
        s3 = boto3.client('s3')
        img_io.seek(0)
        img_io.write(response.content)
        img_content = ContentFile(img_io.getvalue())
        if not settings.DEBUG:
            # in prod saving the image to s3 and later updating the image field via lambda
            s3.put_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=f"media/celery/{file_name}",
                Body=img_io.getvalue()
            )
        else:
            # in dev using celery to process the image
            file.image.save(file_name, img_content)
            file.processed = True
            file.save()
    else:
        file.image.name = file_name
        file.ai_response = response.json()
        file.ai_response['date'] = str(datetime.datetime.now())
        file.processed = True
        file.save()
        raise Exception(str(response.json()))








