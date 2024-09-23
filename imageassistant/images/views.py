from django.shortcuts import render, redirect
from django.urls import reverse
from django.middleware import csrf
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from images.models import Image
from images.forms   import ImageForm, ImageResizeForm
from components.buttons.get_button import GetButton
from components.forms.resize_form import ResizeForm
from components.forms.upload_form import UploadForm
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
            button = UploadForm()
            post_url = reverse('images:add_image')
            attrs = {
                'id': 'upload-form',
                'hx-post': post_url,
                'hx-target': "#img-container",
                "hx-swap": "innerHTML",
                "enctype": "multipart/form-data"
            }
            html_content = button.render(
                kwargs={
                     "attrs": attrs,
                     "errors": form.errors
                }
            )
            return HttpResponse(html_content, content_type='text/html')
    else:
        return HttpResponse("", content_type='text/html')


def get_image(request, image_id):
    image = Image.objects.get(pk=image_id)
    return render(
        request, 'images/initial_image.html', {'image': image}
    )


def get_service_buttons(request, image_id):
    url_context = [
        {
            'url': reverse('images:service', args=[1, image_id]),
            'label': 'Convert to black and white',
            'icon': 'colorize'
        },
        {
            'url': reverse('images:service', args=[2, image_id]),
            'label': 'Remove background',
            'icon': 'lock'
        },
        {
            'url': reverse('images:resize-form-html', args=[image_id]),
            'label': 'Resize',
            'icon': 'transform'
        },
        {
            'url': reverse('images:service', args=[4, image_id]),
            'label': 'Create thumbnail',
            'icon': 'image'
        },
    ]
    html_content = ''
    for context in url_context:
        button = GetButton()
        html_content += button.render(
            args=[context['url'], context['label'], context['icon']]
        )
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
            token = csrf.get_token(request)
            form = ImageResizeForm(request.POST)
            # this is the component that will be rendered
            resize_form = ResizeForm()
            if form.is_valid():
                resize_image.delay(
                    image_id, form.cleaned_data['width'],
                    form.cleaned_data['height']
                )
            else:

                post_url = reverse('images:service', args=[3, image_id])
                data = {
                        'id': 'image-resize-form',
                        'hx-post': post_url,
                        'hx-target': "#img-container",
                        'hx-swap': "innerHTML",
                }
                html_content = resize_form.render(
                    kwargs={
                        "width": request.POST['width'],
                        "height": request.POST['height'],
                        "token": token,
                        "attrs": data,
                        "errors": form.errors
                    }

                )
                return HttpResponse(html_content, content_type='text/html')
    elif service_id == 4:
        print("Creating thumbnail")
        create_thumbnail.delay(image_id)
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
        return render(
            request, 'images/unprocessed_image.html',
            {'image_id': image_id}
        )
    else:
        return render(
            request, 'images/processed_image.html',
            {'file': file}, status=286
        )


def resize_form_html(request, image_id):
    """send a form to the client to get the width and height of the image"""
    token = csrf.get_token(request)
    post_url = reverse('images:service', args=[3, image_id])
    resize_form = ResizeForm()
    data = {
            'id': 'image-resize-form',
            'hx-post': post_url,
            'hx-target': "#img-container",
            'hx-swap': "innerHTML",
    }
    html_content = resize_form.render(
        kwargs={
            "width": '',
            "height": '',
            "token": token,
            "attrs": data,
            "errors": []
        }
    )
    return HttpResponse(html_content, content_type='text/html')
