from django.shortcuts import render, redirect
from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from images.models import Image
from images.forms   import ImageForm, ImageResizeForm
from PIL import Image as PILImage
from .tasks import (
    create_greyscale, remove_background,
    resize_image, create_thumbnail
)
import time
import uuid


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
            <a hx-get="/images/service/1/{image_id}/" hx-indicator="#indicator" hx-target="#img-container"   hx-swap="innerHTML" class="waves-effect waves-light btn custom-img-transform-button" ><span class="material-icons" style="color:black;">autorenew</span>Convert to Black&White</a>
        </div>
        <div class="col s12 m12 l12 xl12  custom-margin-top">
            <a hx-get="/images/service/2/{image_id}/"   hx-indicator="#indicator" hx-target="#img-container"  hx-swap="innerHTML" class="waves-effect waves-light btn custom-img-transform-button" ><span class="material-icons" style="color:black;">lock</span>Remove background</a>
        </div>
        <div class="col s12 m12 l12 xl12  custom-margin-top">
            <a hx-get="/images/resize/form/{image_id}/" hx-swap="innerHTML"    hx-target="#img-container"  class="waves-effect waves-light btn custom-img-transform-button" ><span class="material-icons" style="color:black;">open_with</span>Resize</a>
        </div>
         <div class="col s12 m12 l12 xl12  custom-margin-top">
            <a  hx-get="/images/service/4/{image_id}/" hx-indicator="#indicator" hx-target="#img-container"  hx-swap="innerHTML" class="waves-effect waves-light btn custom-img-transform-button"><span class="material-icons" style="color:black;">image</span>Create Thumbnail</a>
        </div>
    '''
    return HttpResponse(html_content, content_type='text/html')


def service(request, service_id, image_id):
    img = Image.objects.get(pk=image_id)
    img.processed = False
    if service_id == 1:
        print("Creating greyscale image")
        create_greyscale.delay(image_id)
    elif service_id == 2:
        print("Removing background")
        remove_background.delay(image_id)
    elif service_id == 3:
        if request.POST:
            print(request.POST)
            form = ImageResizeForm(request.POST)
            if form.is_valid():
                resize_image.delay(
                    image_id, form.cleaned_data['width'],
                    form.cleaned_data['height']
                )
    elif service_id == 4:
        print("Creating thumbnail")
        create_thumbnail.delay(image_id)
    html_content = f'''
            <div class="col s12 m12 center-align">
                <img class="responsive-img" hx-get="/images/processed/service/{image_id}/" hx-indicator="#indicator" hx-trigger="load delay:1s"  hx-target="#main-content" hx-swap="innerHTML">
            </div>
    '''
        # need to return html so the image container can poll for a processed image
    return HttpResponse(html_content, content_type='text/html')


def processed_service(request, image_id):
    file = Image.objects.get(pk=image_id)
    if not file.processed:
        html_content = f'''
            <img class="responsive-img" hx-get="/images/processed/service/{image_id}/" hx-indicator="#indicator" hx-trigger="load delay:2s"  hx-target="#main-content" hx-swap="innerHTML">
        '''
        return HttpResponse(html_content, content_type='text/html')
    else:
        return HttpResponse(
            f'''
                <div class="row">
                    <div class="col s12 m12 l12 xl12">
                        <a href="{file.image.url}" download="{file.image.url}" class="waves-effect waves-light btn btn-small custom-img-upload-button"><span class="material-icons" style="color:black;margin-top:5px;">download</span>Download</a>
                    </div>
                </div>
                <div class="row">
                    <div class="col s12 m12 l12 xl12">
                        <img src="{file.image.url}" alt="Processed Image" class="responsive-img">
                    </div>
                </div>
            ''', content_type='text/html', status=286)


def resize_form_html(request, image_id):
    """send a form to the client to get the width and height of the image"""
    token = csrf.get_token(request)
    html_content = f'''
            <form id="image-resize-form" hx-post="/images/validate/resize/form/{image_id}/" hx-target="#img-container"  hx-swap="innerHTML">
                <input type="hidden" name="csrfmiddlewaretoken" value={token}>
                <div class="col s12 m12 lg12">
                    <input id="width" name="width" type="number" class="validate">
                    <label for="width">Width in pixels</label>
                </div>
                <div class="col s12 m12 lg12">
                    <input id="height" name="height" type="number" class="validate">
                    <label for="height">Height in pixels</label>
                </div>
                 <div class="col s12 m12 lg12" style="margin-top:5px;">
                    <a  onclick="htmx.trigger('#image-resize-form', 'submit')" class="waves-effect waves-light btn custom-img-transform-button"><span class="material-icons" style="color:white;"></span>Submit</a>
                </div>
            </form>
             
    '''
    return HttpResponse(html_content, content_type='text/html')


def validate_resize_form(request, image_id):
    """ validate the form and return the form with errors or the form with the values"""
    token = csrf.get_token(request)
    form = ImageResizeForm(request.POST)
    if form.is_valid():
        html_content = f'''
            <form id="image-resize-form" hx-post="/images/service/3/{image_id}/" hx-indicator="#indicator" hx-trigger="load"  hx-target="#img-container"  hx-swap="innerHTML">
                <input type="hidden" name="csrfmiddlewaretoken" value={token}>
                <div class="col s12 m12 lg12">
                    <input id="width" name="width" type="number" value={form.cleaned_data['width']}>
                    <label for="width">Width</label>
                </div>
                <div class="col s12 m12 lg12">
                    <input id="height" name="height" type="number" value={form.cleaned_data['height']}>
                    <label for="height">Height</label>
                </div>
            </form>
        '''
        return HttpResponse(html_content, content_type='text/html')
    else:
        errors = "<ul>"
        for k, v in form.errors.items():
            errors += f"<li style='color:red'>{k}: {v}</li>"
        errors += "</ul>"
        html_content = f'''
            <form id="image-resize-form" hx-post="/images/validate/resize/form/{image_id}/" hx-target="#img-container"  hx-swap="innerHTML">
                <input type="hidden" name="csrfmiddlewaretoken" value={token}>
                <div class="col s12 m12 lg=12">
                    <input id="width" name="width" type="number" class="validate" value={request.POST["width"]}>
                    <label for="width">Width</label>
                </div>
                <div class="col s12 m12 lg=12">
                    <input id="height" name="height" type="number" class="validate" value={request.POST["height"]}>
                    <label for="height">Height</label>
                </div>
                 <div class="col s12 m12 lg12" style="margin-top:5px;">
                    <a  onclick="htmx.trigger('#image-resize-form', 'submit')" class="waves-effect waves-light btn custom-img-transform-button"><span class="material-icons" style="color:white;"></span>Submit</a>
                </div>
                {errors}
            </form> 
        '''
        return HttpResponse(html_content, content_type='text/html')
