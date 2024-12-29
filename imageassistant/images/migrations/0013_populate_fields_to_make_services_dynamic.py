from django.db import migrations
from django.conf import settings


def unassign_free_flag_and_description(apps, schema_editor):
    Service = apps.get_model('images', 'Service')
    Service.objects.filter(name='Cropping').delete()
    for service in Service.objects.all():
        service.free = True
        service.description = None
        service.video_url = None
        service.poster_url = None
        service.save()


def populate_free_flag_and_description(apps, schema_editor):
    # cropping service is missing
    Service = apps.get_model('images', 'Service')
    Service.objects.create(
        code=5,
        name='Cropping'
    )
    for service in Service.objects.all():
        if service.name == 'Greyscale':
            service.free = True
            service.description = """Transform your images into classic black-and-white using advanced grayscale techniques. 
            This service is perfect for adding a timeless, artistic feel to photos or preparing images for use in documents, 
            presentations, or websites where a monochrome aesthetic is preferred."""
            service.video_path = f"{settings.MEDIA_URL}video/image_assistant_greyscale_video.mp4"
            service.poster_path = f"{settings.STATIC_URL}img/greyscale_video_thumbnail.png"
        elif service.name == 'Remove Background':
            service.free = False
            service.cost = 5
            service.description = 'This service removes a image background using AI.'
            service.video_path = f"{settings.MEDIA_URL}video/remove_background_demo.mp4"
            service.poster_path = f"{settings.STATIC_URL}img/remove_background.png"
        elif service.name == 'Resize':
            service.description = """Ensure your images fit perfectly for any platform with our high-quality resizing service. 
            We can resize images to specified dimensions while maintaining optimal clarity and resolution.
            Attention! a small image when resized to a larger size may lose quality, in this case try our Image Enhancement service."""
            service.video_path = f"{settings.MEDIA_URL}video/remove_background_demo.mp4"
            service.poster_path = f"{settings.STATIC_URL}img/resizing.png"
        elif service.name == 'Thumbnail':
            service.free = True
            service.description = 'This service takes your image and resizes it to a thumbnail size.'
            service.video_path = f"{settings.MEDIA_URL}video/image_assistant_thumbnail_video.mp4"
            service.poster_path = f"{settings.STATIC_URL}img/thumbnail.png"
        elif service.name == 'Enhancement':
            service.free = False
            service.cost = 3
            service.description = """This service enhances your image using AI. 
            It enhances the image resolution by 4x using predictive and generative AI. 
            Ideal for enhancing the quality of compressed images."""
            service.video_path = f"{settings.MEDIA_URL}video/image_assistant_image_enhance_video.mp4"
            service.poster_path = f"{settings.STATIC_URL}img/image_enhancement.png"
        elif service.name == 'Cropping':
            service.free = True
            service.description = 'This service provides a tool that allows you to crop your image to a specified size.'
            service.video_path = f"{settings.MEDIA_URL}video/image_assistant_crop_video.mp4"
            service.poster_path = f"{settings.STATIC_URL}img/crop_images.png"
        service.save()


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0012_add_in_fields_to_make_services_dynamic'),
    ]

    operations = [
        migrations.RunPython(populate_free_flag_and_description, reverse_code=unassign_free_flag_and_description),
    ]
