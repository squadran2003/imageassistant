from celery import shared_task
from images.models import Image
from PIL import Image as PILImage
from urllib.request import urlopen
from io import BytesIO
from django.core.files.base import ContentFile
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from django.conf import settings




@shared_task
def create_greyscale(image_id):
    s3 = boto3.client('s3')
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
        s3.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=file.image.name,
            Body=img_io.getvalue()
        )
    else:
        file.image.save(file.image.name, img_content)
    file.processed = True
    file.save()


@shared_task
def remove_background(image_id):
    from rembg import remove
    file = Image.objects.get(pk=image_id)
    if not settings.DEBUG:
        img = PILImage.open(urlopen(file.image.url))
    else:
        img = PILImage.open(file.image.path)
    img_io = BytesIO()
    image_bg_removed = remove(img, alpha_matting=True)
    image_bg_removed.save(img_io, format='png')
    img_content = ContentFile(img_io.getvalue())
    file.image.save(file.image.name, img_content)
    file.processed = True
    file.save()
