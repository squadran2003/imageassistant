from celery import shared_task
from PIL import Image as PILImage
from django.core.files.base import ContentFile
from django.conf import settings
import os
from urllib.request import urlopen
from urllib.request import urlopen
from images.models import Image, Service
from io import BytesIO
import cv2
import numpy as np
import urllib
import urllib.parse
import requests
import datetime
import boto3


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
    user = file.user
    service = Service.objects.get(code=2)
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
         # only implement if the feature flag is enabled
        if user.featureflag_set.filter(name='show_credits').exists():
            user.credit.total -= service.tokens
            user.credit.save()
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
def create_image_outline_task(image_id):
    s3 = boto3.client('s3')
    file = Image.objects.get(pk=image_id)
    user = file.user
    file_name = f"{image_id}_outline.png"
    service = Service.objects.get(code=8)
    if not service:
        # catch the error in sentry
        raise Exception("Service not found for code 8 (create Outline)")
    if not settings.DEBUG:
        img = PILImage.open(urlopen(file.image.url))
    else:
        img = PILImage.open(file.image.path)
    try:
        # use cv2 to create an outline of the image
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)

        # Use Canny edge detection for thinner, cleaner lines
        edges = cv2.Canny(blurred, 50, 150)

        # Optional: Apply morphological operations to clean up lines
        kernel = np.ones((2, 2), np.uint8)
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

        # Create a white background (255 = white)
        white_background = np.full_like(edges, 255, dtype=np.uint8)
        
        # Set edge pixels to black (0 = black)
        white_background[edges > 0] = 0

        # Convert to PIL image
        edges_pil = PILImage.fromarray(white_background)
        img_io = BytesIO()
        edges_pil.save(img_io, format='png', quality=100)
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
        # only implement if the feature flag is enabled
        if user.featureflag_set.filter(name='show_credits').exists():
            user.credit.total -= service.tokens
            user.credit.save()
    except Exception as e:
        file.image.name = file_name
        file.ai_response = {
            "error": str(e),
            "date": str(datetime.datetime.now())
        }
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
    service = Service.objects.get(code=7)  # Generate Image service
    if not service:
        # catch the error in sentry
        raise Exception("Service not found for code 7 (Generate Image)")
    user = file.user
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
        # only implement if the feature flag is enabled
        if user.featureflag_set.filter(name='show_credits').exists():
            user.credit.total -= service.tokens
            user.credit.save()
    else:
        file.image.name = file_name
        file.ai_response = response.json()
        file.ai_response['date'] = str(datetime.datetime.now())
        file.processed = True
        file.save()
        raise Exception(str(response.json()))

@shared_task
def delete(image_id):
    file = Image.objects.get(pk=image_id)
    if not settings.DEBUG:
        s3 = boto3.client('s3')
        s3.delete_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=f"media/celery/{image_id}_{file.image.name}"
        )
    else:
        if os.path.isfile(file.image.path):
            os.remove(file.image.path)
    file.delete()


@shared_task
def ping_task():
    return "pong"


@shared_task()
def send_credit_purchase_email(user_email, amount):
    from django.core.mail import send_mail
    subject = "Credit Purchase Confirmation"
    message = f"The {user_email},\n\nhas successfully purchased {amount}.\nyou need to buy from stability AI!"
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.DEFAULT_TO_EMAIL],
        fail_silently=False,
    )


@shared_task
def create_avatar(image_id):
    s3 = boto3.client('s3')
    file = Image.objects.get(pk=image_id)
    user = file.user
    service = Service.objects.get(code=9)  # Avatar Creation service
    if not service:
        raise Exception("Service not found for code 9 (Avatar Creation)")
    
    if not settings.DEBUG:
        img = PILImage.open(urlopen(file.image.url))
    else:
        img = PILImage.open(file.image.path)
    
    img_io = BytesIO()
    img.save(img_io, format='png', quality=100)
    
    # Use Stability AI's image-to-image generation for avatar creation
    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/control/style",
        headers={
            "authorization": f"Bearer {settings.STABILITY_AI_KEY}",
            "accept": "image/*"
        },
        files={"image": img_io.getvalue()},
        data={
            "prompt": "Professional avatar portrait, stylized digital art, clean background, high quality, professional headshot style",
            "strength": 0.5,  # Keep some similarity to original
            "output_format": "png",
            "aspect_ratio": "1:1"
        },
    )
    
    if response.status_code == 200:
        img_io = BytesIO()
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
            
        # only implement if the feature flag is enabled
        if user.featureflag_set.filter(name='show_credits').exists():
            user.credit.total -= service.tokens
            user.credit.save()
    else:
        file.ai_response = {
            "error": f"Avatar creation failed with status {response.status_code}",
            "response": response.text,
            "date": str(datetime.datetime.now())
        }
        file.processed = True
        file.save()
        raise Exception(f"Avatar creation failed: {response.text}")
    
    file.processed = True
    file.save()