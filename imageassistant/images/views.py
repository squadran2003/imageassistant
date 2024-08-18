from django.shortcuts import render, redirect
from django.http import HttpResponse
from images.models import Image
from images.forms   import ImageForm
from PIL import Image as PILImage
from .tasks import create_greyscale, remove_background
import time


# maps to celery task functions
# service_choices = [
#     (1, 'convert to greyscale'),
#     (2, 'Remove background'),
#     (3, 'Resize'),
# ]


def add_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            img.save()
            return redirect("images:get_image", image_id=img.id)
        else:
            print(form.errors)
            return HttpResponse("", content_type='text/html')
    else:
        return HttpResponse("", content_type='text/html')


def get_image(request, image_id):
    image = Image.objects.get(pk=image_id)
    html_content = f'''
        <img src="{image.image.url}" alt="Processed Image" class="responsive-img" hx-target="#service-buttons" hx-trigger="load" hx-get="/images/services/buttons/{image_id}" hx-swap="innerHTML">
    '''
    return HttpResponse(html_content, content_type='text/html')


def get_service_buttons(request, image_id):
    """when the image load I need to set the buttons with the correct service and image id so the backend knows what image its processing"""
    html_content = f'''
        <div class="col s12 m12 l12 xl12  custom-margin-top">
            <a hx-get="/images/service/1/{image_id}" hx-indicator="#indicator" hx-target="#img-container"   hx-swap="innerHTML" class="waves-effect waves-light btn custom-img-transform-button" ><span class="material-icons" style="color:white;">autorenew</span>Convert to Black&White</a>
        </div>
        <div class="col s12 m12 l12 xl12  custom-margin-top">
            <a hx-get="/images/service/2/{image_id}"   hx-indicator="#indicator" hx-target="#img-container"  hx-swap="innerHTML" class="waves-effect waves-light btn custom-img-transform-button" ><span class="material-icons" style="color:white;">remove</span>Remove background</a>
        </div>
        <div class="col s12 m12 l12 xl12  custom-margin-top">
            <a hx-get="/images/service/3/{image_id}"   hx-indicator="#indicator" hx-target="#img-container"  hx-swap="innerHTML" class="waves-effect waves-light btn custom-img-transform-button" ><span class="material-icons" style="color:white;">open_with</span>Resize</a>
        </div>
    '''
    return HttpResponse(html_content, content_type='text/html')


def service(request, service_id, image_id):
    image = Image.objects.get(pk=image_id)
    image.processed = False
    image.save()
    if service_id == 1:
        print("Creating greyscale image")
        create_greyscale.delay(image_id)
    elif service_id == 2:
        print("Removing background")
        remove_background.delay(image_id)
    html_content = f'''
            <div class="col s12 m12 center-align">
                <img class="responsive-img" hx-get="/images/processed/service/{image_id}/" hx-indicator="#indicator" hx-trigger="load delay:1s"  hx-target="#img-container" hx-swap="innerHTML">
            </div>
    '''
        # need to return html so the image container can poll for a processed image
    return HttpResponse(html_content, content_type='text/html')


def processed_service(request, image_id):
    file = Image.objects.get(pk=image_id)
    if not file.processed:
        html_content = f'''
            <img class="responsive-img" hx-get="/images/processed/service/{image_id}/" hx-indicator="#indicator" hx-trigger="load delay:1s"  hx-target="#img-container" hx-swap="innerHTML">
        '''
        return HttpResponse(html_content, content_type='text/html')
    else:
        return HttpResponse(
            f'''
                <img src="{file.image.url}" alt="Processed Image" class="responsive-img">
                <a href="{file.image.url}" download="{file.image.url}" class="waves-effect waves-light btn btn-small custom-img-transform-button download-button"><span class="material-icons" style="color:white;margin-top:5px;">download</span>Download</a>
            ''', content_type='text/html', status=286)