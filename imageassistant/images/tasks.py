from celery import shared_task
from images.models import Image
from PIL import Image as PILImage
from io import BytesIO
from django.core.files.base import ContentFile




@shared_task
def create_greyscale(image_id):
    file = Image.objects.get(pk=image_id)
    img = PILImage.open(file.image.path)
    grayscale_img = img.convert("L")
    # Save the grayscale image to a BytesIO object
    img_io = BytesIO()
    grayscale_img.save(img_io, format='png')
    img_content = ContentFile(img_io.getvalue())
    # dont want a new folder , just want to override the uploaded image
    file.image.save(file.image.name, img_content)
    file.processed = True
    file.save()


@shared_task
def remove_background(image_id):
    from rembg import remove
    file = Image.objects.get(pk=image_id)
    img = PILImage.open(file.image.path)
    img_io = BytesIO()
    image_bg_removed = remove(img, alpha_matting=True)
    image_bg_removed.save(img_io, format='png')
    img_content = ContentFile(img_io.getvalue())
    file.image.save(file.image.name, img_content)
    file.processed = True
    file.save()